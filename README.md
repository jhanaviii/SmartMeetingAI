# SmartMeetingAI

A modern, AI-powered meeting invitation generator and distribution system built with Flask and OpenAI.

## Project Structure

```
SmartMeetingAI/
├── backend/
│   ├── .env                    # Environment variables (create this)
│   ├── config.py              # Application configuration
│   ├── db.py                  # Database connection handler
│   ├── main.py                # Main Flask application with routes
│   ├── requirements.txt       # Python dependencies
│   ├── env.example           # Environment variables template
│   └── utils/
│       ├── __init__.py
│       ├── models.py          # Database models
│       ├── validation.py      # Input validation utilities
│       ├── template_generator.py  # AI template generation
│       ├── email_service.py   # Gmail integration
│       └── whatsapp_service.py # WhatsApp integration
├── frontend/
│   └── templates/
│       ├── base.html          # Base template
│       ├── auth.html          # Login/Register page
│       ├── dashboard.html     # Main dashboard
│       ├── template_generator.html  # Template creation
│       ├── distribution.html  # Invitation distribution
│       └── settings.html      # User settings
├── .gitignore                 # Git ignore rules
├── API_KEYS_DOCUMENTATION.md  # API keys documentation
└── README.md                  # This file
```

## Features

- 🤖 **AI-Powered Templates**: Generate professional meeting invitations using OpenAI
- 📧 **Gmail Integration**: Send invitations directly via Gmail
- 📱 **WhatsApp Integration**: Send invitations via WhatsApp Business API
- 📊 **Dashboard Analytics**: Track templates, invitations, and success rates
- 🔐 **User Authentication**: Secure login and registration system
- 📱 **Responsive Design**: Modern, mobile-friendly interface
- 🎨 **Beautiful UI**: Professional gradient design with smooth animations

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Gmail account (for email sending)
- WhatsApp Business API (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartMeetingAI
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys (see API_KEYS_DOCUMENTATION.md)
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5001`
   - Register a new account or log in
   - Start creating AI-powered meeting invitations!

## API Keys Setup

Before running the application, you need to set up the following API keys in your `.env` file:

1. **OpenAI API Key**: For AI-powered template generation
2. **Gmail App Password**: For sending email invitations
3. **WhatsApp Business API** (optional): For WhatsApp messaging

See `API_KEYS_DOCUMENTATION.md` for detailed setup instructions.

## Usage

### Creating Templates

1. Navigate to "Template Generator"
2. Fill in meeting details (topic, speaker, date, time, etc.)
3. Click "Generate Template" to create an AI-powered invitation
4. Preview and customize the generated template
5. Save the template for later use

### Sending Invitations

1. Go to "Distribution" page
2. Select a saved template
3. Choose distribution method (Gmail or WhatsApp)
4. Enter recipient information
5. Send invitations with one click

### Managing Settings

1. Access "Settings" page
2. Configure Gmail integration
3. Set up WhatsApp Business API
4. Manage AI model preferences
5. Update account information

## Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **OpenAI**: AI template generation
- **SMTP**: Email sending
- **WhatsApp Business API**: Messaging

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive design
- **Font Awesome**: Icons
- **Google Fonts**: Typography

### Database
- **SQLite**: Lightweight database (can be upgraded to PostgreSQL/MySQL)

## Development

### Project Structure Benefits

- **Separation of Concerns**: Backend and frontend are clearly separated
- **Modular Design**: Utils directory contains reusable business logic
- **Clean Architecture**: Database models, services, and controllers are organized
- **Easy Maintenance**: Each component has a single responsibility
- **Scalability**: Easy to add new features and integrations

### Adding New Features

1. **Backend**: Add routes in `main.py`, business logic in `utils/`
2. **Frontend**: Create new templates in `frontend/templates/`
3. **Database**: Add models in `utils/models.py`

## Deployment

### Production Setup

1. **Environment Variables**: Set production API keys
2. **Database**: Use PostgreSQL or MySQL for production
3. **Web Server**: Use Gunicorn with Nginx
4. **SSL**: Enable HTTPS with Let's Encrypt
5. **Monitoring**: Set up logging and error tracking

### Docker Deployment

```dockerfile
# Example Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "backend/main.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the API documentation
- Review the troubleshooting guide
- Open an issue on GitHub

---

**SmartMeetingAI** - Making meeting coordination smarter with AI! 🤖📅
