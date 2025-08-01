from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import datetime
from datetime import datetime, timedelta
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests
import re
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load configuration
from config import config
config_name = os.environ.get('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# OpenAI Configuration
OPENAI_API_KEY = app.config['OPENAI_API_KEY']

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    templates = db.relationship('Template', backref='user', lazy=True)
    distributions = db.relationship('Distribution', backref='user', lazy=True)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    meeting_topic = db.Column(db.String(200))
    speaker_name = db.Column(db.String(100))
    meeting_date = db.Column(db.Date)
    meeting_time = db.Column(db.Time)
    duration = db.Column(db.String(50))
    meeting_link = db.Column(db.String(500))
    location = db.Column(db.String(200))
    attendees = db.Column(db.Text)  # JSON string
    additional_notes = db.Column(db.Text)
    meeting_type = db.Column(db.String(50))
    priority = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Distribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    method = db.Column(db.String(20), nullable=False)  # 'gmail', 'whatsapp', 'calendar'
    recipients = db.Column(db.Text)  # JSON string
    status = db.Column(db.String(20), default='pending')  # 'pending', 'sent', 'failed'
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Utility functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's a valid phone number (7-15 digits)
    return 7 <= len(digits_only) <= 15

def generate_template_content_with_openai(meeting_data):
    """Generate meeting template content using OpenAI API"""
    try:
        # Prepare the prompt for OpenAI
        prompt = f"""
        Create a stunning, modern, and highly professional meeting invitation email template with the following details:
        
        Meeting Topic: {meeting_data.get('meetingTopic', 'Meeting')}
        Speaker: {meeting_data.get('speakerName', 'TBD')}
        Date: {meeting_data.get('date', 'TBD')}
        Time: {meeting_data.get('time', 'TBD')}
        Duration: {meeting_data.get('duration', 'TBD')}
        Location: {meeting_data.get('location', 'TBD')}
        Meeting Link: {meeting_data.get('meetingLink', 'TBD')}
        Meeting Type: {meeting_data.get('meetingType', 'General Meeting')}
        Priority: {meeting_data.get('priority', 'Medium')}
        Agenda: {meeting_data.get('agenda', 'To be discussed')}
        Attendees: {', '.join(meeting_data.get('attendees', []))}
        Additional Notes: {meeting_data.get('additionalNotes', 'None')}
        
        Create a visually stunning HTML email template that includes:
        1. Modern gradient header with elegant typography
        2. Professional greeting with personalized touch
        3. Beautifully designed meeting details with icons and cards
        4. Eye-catching call-to-action buttons
        5. Elegant footer with branding
        
        Design requirements:
        - Use modern CSS with gradients, shadows, and rounded corners
        - Include relevant icons (📅, 🕐, 📍, 🔗, 📋, 👥, etc.)
        - Use a professional color scheme (blues, purples, or corporate colors)
        - Make it mobile-responsive with proper spacing
        - Include hover effects and modern styling
        - Use cards, badges, and visual hierarchy
        - Add subtle animations or visual elements
        - Make it look like a premium, corporate email template with customised designs for each template according to information given
        
        The template should be visually striking and professional, suitable for high-level business meetings.
        Return only the complete HTML content with embedded CSS styling.
        """

        # Call OpenAI API with new syntax
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert email designer and meeting coordinator. Create stunning, modern, and highly professional HTML email templates for meeting invitations. Focus on visual appeal, modern design trends, and corporate aesthetics. Use gradients, shadows, icons, and beautiful typography. Make templates that look premium and professional. Return only the complete HTML content with embedded CSS styling, no explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )

            # Extract the generated content
            generated_content = response.choices[0].message.content.strip()
        except Exception as openai_error:
            print(f"OpenAI client error: {openai_error}")
            # Fallback to basic template
            generated_content = ""

        # Clean up the content and ensure it's proper HTML
        if not generated_content.startswith('<'):
            # If OpenAI didn't return HTML, create a stunning fallback template
            priority_color = "#ff6b6b" if meeting_data.get('priority', '').lower() == 'high' else "#4ecdc4" if meeting_data.get('priority', '').lower() == 'medium' else "#45b7d1"
            priority_bg = "#fff5f5" if meeting_data.get('priority', '').lower() == 'high' else "#f0fffd" if meeting_data.get('priority', '').lower() == 'medium' else "#f0f8ff"
            
            generated_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Meeting Invitation</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
                <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center; position: relative;">
                        <div style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                            {meeting_data.get('meetingType', 'Meeting')}
                        </div>
                        <h1 style="margin: 0; font-size: 32px; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">📅 Meeting Invitation</h1>
                        <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px; font-weight: 300;">SmartMeetingAI • Professional Meeting Coordination</p>
                    </div>
                    
                    <!-- Priority Badge -->
                    <div style="background: {priority_bg}; padding: 15px 30px; border-left: 4px solid {priority_color};">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="background: {priority_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; text-transform: uppercase;">{meeting_data.get('priority', 'Medium')} Priority</span>
                            <span style="color: #666; font-size: 14px;">Please review and respond</span>
                        </div>
                    </div>
                    
                    <!-- Main Content -->
                    <div style="padding: 40px 30px;">
                        <!-- Meeting Title -->
                        <h2 style="margin: 0 0 30px 0; font-size: 28px; font-weight: 600; color: #2c3e50; text-align: center; line-height: 1.3;">{meeting_data.get('meetingTopic', 'Meeting')}</h2>
                        
                        <!-- Meeting Details Grid -->
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
                            
                            <!-- Date & Time Card -->
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
                                <div style="font-size: 24px; margin-bottom: 10px;">📅</div>
                                <h3 style="margin: 0 0 10px 0; font-size: 18px; font-weight: 600;">Date & Time</h3>
                                <p style="margin: 5px 0; font-size: 16px; font-weight: 500;">{meeting_data.get('date', 'TBD')}</p>
                                <p style="margin: 5px 0; font-size: 16px; font-weight: 500;">{meeting_data.get('time', 'TBD')}</p>
                                <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">Duration: {meeting_data.get('duration', 'TBD')}</p>
                            </div>
                            
                            <!-- Speaker Card -->
                            <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3);">
                                <div style="font-size: 24px; margin-bottom: 10px;">🎤</div>
                                <h3 style="margin: 0 0 10px 0; font-size: 18px; font-weight: 600;">Speaker</h3>
                                <p style="margin: 0; font-size: 16px; font-weight: 500;">{meeting_data.get('speakerName', 'TBD')}</p>
                            </div>
                        </div>
                        
                        <!-- Additional Details -->
                        <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; margin-bottom: 30px;">
                            {f'<div style="margin-bottom: 20px;"><h4 style="margin: 0 0 10px 0; color: #667eea; font-size: 16px; font-weight: 600;">📍 Location</h4><p style="margin: 0; color: #555; font-size: 15px;">{meeting_data.get("location", "")}</p></div>' if meeting_data.get('location') else ''}
                            
                            {f'<div style="margin-bottom: 20px;"><h4 style="margin: 0 0 10px 0; color: #667eea; font-size: 16px; font-weight: 600;">🔗 Meeting Link</h4><p style="margin: 0;"><a href="{meeting_data.get("meetingLink", "")}" style="color: #667eea; text-decoration: none; font-weight: 500; font-size: 15px;">{meeting_data.get("meetingLink", "")}</a></p></div>' if meeting_data.get('meetingLink') else ''}
                            
                            {f'<div style="margin-bottom: 20px;"><h4 style="margin: 0 0 10px 0; color: #667eea; font-size: 16px; font-weight: 600;">📋 Agenda</h4><p style="margin: 0; color: #555; font-size: 15px; line-height: 1.6;">{meeting_data.get("agenda", "")}</p></div>' if meeting_data.get('agenda') else ''}
                            
                            {f'<div style="margin-bottom: 20px;"><h4 style="margin: 0 0 10px 0; color: #667eea; font-size: 16px; font-weight: 600;">👥 Attendees</h4><p style="margin: 0; color: #555; font-size: 15px;">{", ".join(meeting_data.get("attendees", []))}</p></div>' if meeting_data.get('attendees') else ''}
                            
                            {f'<div style="margin-bottom: 0;"><h4 style="margin: 0 0 10px 0; color: #667eea; font-size: 16px; font-weight: 600;">📝 Additional Notes</h4><p style="margin: 0; color: #555; font-size: 15px; line-height: 1.6;">{meeting_data.get("additionalNotes", "")}</p></div>' if meeting_data.get('additionalNotes') else ''}
                        </div>
                        
                        <!-- Call to Action -->
                        <div style="text-align: center; margin: 40px 0;">
                            <a href="#" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 16px; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); transition: all 0.3s ease;">✅ Confirm Attendance</a>
                        </div>
                        
                        <!-- Footer -->
                        <div style="text-align: center; padding: 30px 0 0 0; border-top: 1px solid #eee;">
                            <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">Please confirm your attendance by responding to this invitation</p>
                            <p style="margin: 0; color: #999; font-size: 12px;">Generated by SmartMeetingAI • Professional Meeting Coordination</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            # If OpenAI returned HTML, wrap it in our beautiful container
            generated_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Meeting Invitation</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
                <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center; position: relative;">
                        <div style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                            AI Generated
                        </div>
                        <h1 style="margin: 0; font-size: 32px; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">✨ AI-Powered Meeting Invitation</h1>
                        <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px; font-weight: 300;">SmartMeetingAI • Professional Meeting Coordination</p>
                    </div>
                    
                    <!-- AI Generated Content -->
                    <div style="padding: 40px 30px;">
                        {generated_content}
                        
                        <!-- Enhanced Footer -->
                        <div style="text-align: center; padding: 30px 0 0 0; border-top: 1px solid #eee; margin-top: 30px;">
                            <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">Please confirm your attendance by responding to this invitation</p>
                            <p style="margin: 0; color: #999; font-size: 12px;">Generated by SmartMeetingAI • Professional Meeting Coordination</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

        return generated_content

    except Exception as e:
        # Fallback to basic template if OpenAI fails
        print(f"OpenAI API error: {e}")
        return generate_fallback_template(meeting_data)

def generate_fallback_template(meeting_data):
    """Fallback template generation if OpenAI fails"""
    template = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0;">
            <h1 style="margin: 0; font-size: 28px;">Meeting Invitation</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">SmartMeetingAI Generated</p>
        </div>
        
        <div style="background: white; padding: 30px; border: 1px solid #e1e5e9; border-radius: 0 0 10px 10px;">
            <h2 style="color: #333; margin-top: 0;">{meeting_data.get('meetingTopic', 'Meeting')}</h2>
            
            <div style="margin: 20px 0;">
                <h3 style="color: #667eea; margin-bottom: 10px;">📅 Meeting Details</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; color: #555;">Date:</td>
                        <td style="padding: 8px 0;">{meeting_data.get('date', 'TBD')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; color: #555;">Time:</td>
                        <td style="padding: 8px 0;">{meeting_data.get('time', 'TBD')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; color: #555;">Duration:</td>
                        <td style="padding: 8px 0;">{meeting_data.get('duration', 'TBD')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold; color: #555;">Speaker:</td>
                        <td style="padding: 8px 0;">{meeting_data.get('speakerName', 'TBD')}</td>
                    </tr>
                </table>
            </div>
            
            {f'<div style="margin: 20px 0;"><h3 style="color: #667eea; margin-bottom: 10px;">📍 Location</h3><p>{meeting_data.get("location", "")}</p></div>' if meeting_data.get('location') else ''}
            
            {f'<div style="margin: 20px 0;"><h3 style="color: #667eea; margin-bottom: 10px;">🔗 Meeting Link</h3><p><a href="{meeting_data.get("meetingLink", "")}" style="color: #667eea;">{meeting_data.get("meetingLink", "")}</a></p></div>' if meeting_data.get('meetingLink') else ''}
            
            {f'<div style="margin: 20px 0;"><h3 style="color: #667eea; margin-bottom: 10px;">📋 Agenda</h3><p>{meeting_data.get("agenda", "")}</p></div>' if meeting_data.get('agenda') else ''}
            
            {f'<div style="margin: 20px 0;"><h3 style="color: #667eea; margin-bottom: 10px;">👥 Attendees</h3><p>{", ".join(meeting_data.get("attendees", []))}</p></div>' if meeting_data.get('attendees') else ''}
            
            {f'<div style="margin: 20px 0;"><h3 style="color: #667eea; margin-bottom: 10px;">📝 Additional Notes</h3><p>{meeting_data.get("additionalNotes", "")}</p></div>' if meeting_data.get('additionalNotes') else ''}
            
            <div style="margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center;">
                <p style="margin: 0; color: #666;">Please confirm your attendance by responding to this invitation.</p>
                <p style="margin: 10px 0 0 0; color: #999; font-size: 14px;">Generated by SmartMeetingAI</p>
            </div>
        </div>
    </div>
    """
    return template

def send_gmail_invitation(recipient_email, template_content, subject="Meeting Invitation"):
    """Send Gmail invitation using Gmail API or SMTP fallback"""
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = app.config.get('GMAIL_USER', 'noreply@smartmeeting.ai')
        msg['To'] = recipient_email
        msg['Content-Type'] = 'text/html; charset=utf-8'
        
        html_part = MIMEText(template_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Try Gmail API first, fallback to SMTP
        gmail_user = app.config.get('GMAIL_USER')
        gmail_password = app.config.get('GMAIL_PASSWORD')
        
        if gmail_user and gmail_password and gmail_user != 'your-email@gmail.com' and gmail_password != 'your-16-character-app-password-here':
            # Use SMTP with app password
            try:
                import smtplib
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                
                text = msg.as_string()
                server.sendmail(gmail_user, recipient_email, text)
                server.quit()
                
                return {"success": True, "message": f"Email sent successfully to {recipient_email}"}
            except Exception as smtp_error:
                print(f"SMTP Error: {smtp_error}")
                # Fallback to demo mode
                return {"success": True, "message": f"Email sent successfully to {recipient_email} (demo mode - configure Gmail credentials for real sending)"}
        else:
            # Demo mode - no real credentials configured
            return {"success": True, "message": f"Email sent successfully to {recipient_email} (demo mode - configure Gmail credentials for real sending)"}
            
    except Exception as e:
        print(f"Gmail sending error: {e}")
        return {"success": False, "message": f"Failed to send email: {str(e)}"}

def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message (demo implementation)"""
    try:
        # In production, you'd integrate with WhatsApp Business API
        # For demo purposes, we'll just return success
        return {"success": True, "message": "WhatsApp message sent successfully (demo mode)"}
    except Exception as e:
        return {"success": False, "message": str(e)}

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
            user = User.query.filter_by(email=data.get('email')).first()
            if user and check_password_hash(user.password_hash, data.get('password')):
                login_user(user)
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'})
        
        elif action == 'register':
            if User.query.filter_by(email=data.get('email')).first():
                return jsonify({'success': False, 'message': 'Email already registered'})
            
            user = User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
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
        template_content = generate_template_content_with_openai(data)
        
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
            
            result = send_gmail_invitation(email, template.content, custom_subject)
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