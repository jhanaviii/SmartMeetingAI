# SmartMeetingAI - Production Ready Flask Application

A modern Flask-based web application for generating and distributing professional meeting invitations with AI assistance using OpenAI's GPT models.

## Features

- **AI-Powered Template Generation**: Create professional meeting invitations using OpenAI GPT-3.5-turbo
- **Multi-Channel Distribution**: Send invitations via Gmail and WhatsApp
- **User Authentication**: Secure login and registration system
- **Dashboard Analytics**: Track templates generated and invitations sent
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- **Database Storage**: SQLite database for storing templates and distribution history
- **Production Ready**: Configured for production deployment with Gunicorn

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Template Engine**: Jinja2
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Production Server**: Gunicorn

## Quick Start (Development)

1. **Clone the repository**
```bash
git clone <repository-url>
cd SmartMeetingAI
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp env.example .env
# Edit .env file with your OpenAI API key and other settings
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
Open your browser and navigate to `http://localhost:5001`

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set environment variables**
```bash
export FLASK_ENV=production
export OPENAI_API_KEY=your-openai-api-key
export SECRET_KEY=your-secret-key
```

3. **Run with Gunicorn**
```bash
gunicorn -c gunicorn.conf.py app:app
```

### Using the production script

```bash
python run.py
```

### Using Docker (Optional)

```bash
docker build -t smartmeeting-ai .
docker run -p 5001:5001 -e OPENAI_API_KEY=your-key smartmeeting-ai
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Application Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///smartmeeting.db

# OpenAI Configuration (Required)
OPENAI_API_KEY=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

# Gmail Integration (Optional)
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password

# WhatsApp Integration (Optional)
WHATSAPP_API_KEY=your-whatsapp-api-key
WHATSAPP_PHONE_NUMBER=your-whatsapp-phone-number

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

## Usage

1. **Register/Login**: Create an account or sign in to access the application
2. **Create Templates**: Use the Template Generator to create AI-powered meeting invitations
3. **Send Invitations**: Distribute templates via Gmail or WhatsApp
4. **Monitor Activity**: View statistics and recent activity on the dashboard
5. **Manage Settings**: Configure integrations and notification preferences

## Project Structure

```
SmartMeetingAI/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── run.py                 # Production startup script
├── gunicorn.conf.py       # Gunicorn configuration
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── auth.html         # Authentication pages
│   ├── dashboard.html    # Dashboard page
│   ├── template_generator.html  # Template creation
│   ├── distribution.html # Distribution page
│   └── settings.html     # Settings page
├── uploads/              # File uploads directory
├── static/               # Static files (CSS, JS)
└── README.md            # This file
```

## API Endpoints

- `GET /` - Dashboard (requires authentication)
- `GET /auth` - Authentication page
- `POST /auth` - Login/Register
- `GET /template-generator` - Template creation page
- `POST /api/templates/generate` - Generate AI-powered template
- `GET /distribution` - Distribution page
- `POST /api/distribution/gmail` - Send Gmail invitation
- `POST /api/distribution/whatsapp` - Send WhatsApp invitation
- `GET /settings` - Settings page
- `GET /api/health` - Health check endpoint

## Database Models

- **User**: User accounts and authentication
- **Template**: Generated meeting templates with AI content
- **Distribution**: Distribution history and status

## AI Integration

The application uses OpenAI's GPT-3.5-turbo model to generate professional meeting invitation templates. The AI:

- Creates contextually relevant content based on meeting details
- Generates professional HTML email templates
- Includes proper formatting and styling
- Adapts content based on meeting type, priority, and attendees

## Production Features

- **Gunicorn Configuration**: Optimized for production deployment
- **Environment-based Configuration**: Separate dev/prod settings
- **Error Handling**: Comprehensive error handling and logging
- **Security**: Production-ready security settings
- **Health Checks**: Built-in health check endpoint
- **Database Management**: Automatic table creation and migration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on GitHub. 