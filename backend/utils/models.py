from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Global db instance that will be set by init_models
db = None

def init_models(db_instance):
    """Initialize models with database instance"""
    global db
    db = db_instance
    
    # Define models as classes that will be created with the db instance
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
    
    # Return the model classes
    return User, Template, Distribution 