from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import datetime
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration and database
from config import config
from db import init_db, get_db

# Import utility functions
from utils.validation import validate_email, validate_phone
from utils.template_generator import generate_template_content_with_openai
from utils.email_service import send_gmail_invitation
from utils.whatsapp_service import send_whatsapp_message

app = Flask(__name__, template_folder='../frontend/templates')

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# OpenAI Configuration
OPENAI_API_KEY = app.config['OPENAI_API_KEY']

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = init_db(app)

# Initialize models with database instance
from utils.models import init_models
User, Template, Distribution = init_models(db)

# Create database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")
        
        # Create a demo user if none exists
        if not User.query.first():
            demo_user = User(
                username='demo_user',
                email='demo@example.com',
                password_hash=generate_password_hash('demo123')
            )
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created: demo@example.com / demo123")
            
    except Exception as e:
        print(f"Database initialization warning: {e}")

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    # Get statistics
    stats = {
        'templates_generated': Template.query.filter_by(user_id=current_user.id).count(),
        'invitations_sent': Distribution.query.filter_by(user_id=current_user.id, status='sent').count(),
        'total_recipients': sum(len(json.loads(d.recipients)) for d in Distribution.query.filter_by(user_id=current_user.id)),
        'calendar_events': Distribution.query.filter_by(user_id=current_user.id, method='calendar').count(),
        'success_rate': 94.2,  # Mock data
        'recent_activity': []
    }
    
    # Get recent distributions
    recent_distributions = Distribution.query.filter_by(user_id=current_user.id).order_by(Distribution.created_at.desc()).limit(5).all()
    
    for dist in recent_distributions:
        template = db.session.get(Template, dist.template_id)
        stats['recent_activity'].append({
            'id': dist.id,
            'type': 'invitation_sent',
            'title': template.title if template else 'Unknown Template',
            'description': f'Sent via {dist.method}',
            'timestamp': dist.created_at,
            'status': dist.status
        })
    
    return render_template('dashboard.html', stats=stats)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        
        if action == 'login':
            # Bypass authentication - allow any login
            email = data.get('email', 'demo@example.com')
            password = data.get('password', 'demo123')
            
            # Check if user exists, if not create one
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    username=email.split('@')[0],
                    email=email,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        
        elif action == 'register':
            email = data.get('email', 'demo@example.com')
            username = data.get('username', 'demo_user')
            password = data.get('password', 'demo123')
            
            # Check if user exists, if not create one
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return render_template('auth.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

@app.route('/template-generator')
@login_required
def template_generator():
    return render_template('template_generator.html')

@app.route('/api/templates/generate', methods=['POST'])
@login_required
def generate_template():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['meetingTopic', 'speakerName', 'date', 'time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate template content using OpenAI
        template_content = generate_template_content_with_openai(data, OPENAI_API_KEY)
        
        # Save template to database
        template = Template(
            title=data['meetingTopic'],
            content=template_content,
            meeting_topic=data['meetingTopic'],
            speaker_name=data['speakerName'],
            meeting_date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            meeting_time=datetime.strptime(data['time'], '%H:%M').time(),
            duration=data.get('duration'),
            meeting_link=data.get('meetingLink'),
            location=data.get('location'),
            attendees=json.dumps(data.get('attendees', [])),
            additional_notes=data.get('additionalNotes'),
            meeting_type=data.get('meetingType'),
            priority=data.get('priority'),
            user_id=current_user.id
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'template': template_content,
            'template_id': template.id,
            'message': 'Template generated successfully using AI'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/distribution')
@login_required
def distribution():
    templates = Template.query.filter_by(user_id=current_user.id).all()
    return render_template('distribution.html', templates=templates)

@app.route('/api/distribution/gmail', methods=['POST'])
@login_required
def send_gmail():
    try:
        data = request.get_json()
        recipient_emails = data.get('recipientEmails', [])
        recipient_email = data.get('recipientEmail')  # Backward compatibility
        template_id = data.get('templateId')
        subject = data.get('subject', 'Meeting Invitation')
        
        # Handle both single email and multiple emails
        if recipient_email and not recipient_emails:
            recipient_emails = [recipient_email]
        
        if not recipient_emails or not template_id:
            return jsonify({'error': 'Recipient email(s) and template ID are required'}), 400
        
        # Validate all emails
        invalid_emails = [email for email in recipient_emails if not validate_email(email)]
        if invalid_emails:
            return jsonify({'error': f'Invalid email format(s): {", ".join(invalid_emails)}'}), 400
        
        template = db.session.get(Template, template_id)
        if not template or template.user_id != current_user.id:
            return jsonify({'error': 'Template not found'}), 404
        
        # Send emails to all recipients
        results = []
        successful_sends = 0
        
        for email in recipient_emails:
            # Customize subject with meeting topic if available
            custom_subject = f"{subject}: {template.meeting_topic}" if template.meeting_topic else subject
            
            result = send_gmail_invitation(
                email, 
                template.content, 
                custom_subject,
                app.config.get('GMAIL_USER'),
                app.config.get('GMAIL_PASSWORD')
            )
            results.append({
                'email': email,
                'success': result['success'],
                'message': result['message']
            })
            
            if result['success']:
                successful_sends += 1
        
        # Save distribution record
        distribution = Distribution(
            template_id=template_id,
            method='gmail',
            recipients=json.dumps([{'email': email} for email in recipient_emails]),
            status='sent' if successful_sends > 0 else 'failed',
            sent_at=datetime.utcnow(),
            user_id=current_user.id
        )
        db.session.add(distribution)
        db.session.commit()
        
        # Return summary
        if successful_sends == len(recipient_emails):
            return jsonify({
                'success': True,
                'message': f'Successfully sent {successful_sends} invitation(s)',
                'details': results
            })
        elif successful_sends > 0:
            return jsonify({
                'success': True,
                'message': f'Partially successful: {successful_sends}/{len(recipient_emails)} sent',
                'details': results
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send any invitations',
                'details': results
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/distribution/whatsapp', methods=['POST'])
@login_required
def send_whatsapp():
    try:
        data = request.get_json()
        phone_number = data.get('phoneNumber')
        template_id = data.get('templateId')
        
        if not phone_number or not template_id:
            return jsonify({'error': 'Phone number and template ID are required'}), 400
        
        if not validate_phone(phone_number):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        template = db.session.get(Template, template_id)
        if not template or template.user_id != current_user.id:
            return jsonify({'error': 'Template not found'}), 404
        
        # Send WhatsApp message
        result = send_whatsapp_message(phone_number, template.content)
        
        # Save distribution record
        distribution = Distribution(
            template_id=template_id,
            method='whatsapp',
            recipients=json.dumps([{'phone': phone_number}]),
            status='sent' if result['success'] else 'failed',
            sent_at=datetime.utcnow(),
            user_id=current_user.id
        )
        db.session.add(distribution)
        db.session.commit()
        
        return jsonify({
            'success': result['success'],
            'message': result['message']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/api/templates/<int:template_id>/download')
@login_required
def download_template(template_id):
    """Download template as HTML file"""
    try:
        template = db.session.get(Template, template_id)
        if not template or template.user_id != current_user.id:
            return jsonify({'error': 'Template not found'}), 404
        
        # Create HTML content with proper styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{template.title}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    line-height: 1.6; 
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 30px; 
                    text-align: center;
                }}
                .content {{ 
                    padding: 30px; 
                }}
                .footer {{ 
                    margin-top: 20px; 
                    text-align: center; 
                    color: #666; 
                    font-size: 14px; 
                    padding: 20px;
                    background: #f8f9fa;
                }}
                .meeting-details {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .meeting-details h3 {{
                    color: #667eea;
                    margin-top: 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                td {{
                    padding: 8px 0;
                }}
                td:first-child {{
                    font-weight: bold;
                    color: #555;
                    width: 30%;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {template.content}
                <div class="footer">
                    <p>Generated by SmartMeetingAI</p>
                    <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create response with HTML file
        from io import BytesIO
        response = send_file(
            BytesIO(html_content.encode('utf-8')),
            mimetype='text/html',
            as_attachment=True,
            download_name=f"{template.title.replace(' ', '_')}_meeting_invitation.html"
        )
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'module': 'SmartMeetingAI Flask'
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=5001) 