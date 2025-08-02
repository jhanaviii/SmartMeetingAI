# SmartMeetingAI Setup Guide

## Project Structure ✅

The project now follows the exact structure you specified:

```
/Module_(X)_Routes
├── backend/
│   ├── .env                    # Environment variables (create this)
│   ├── db.py                   # Database connection handler
│   ├── main.py                 # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Startup script
│   ├── env.example            # Environment template
│   └── utils/
│       ├── __init__.py
│       ├── models.py           # Database models
│       ├── validation.py       # Input validation
│       ├── template_generator.py  # AI template generation
│       ├── email_service.py    # Gmail integration
│       └── whatsapp_service.py # WhatsApp integration
├── frontend/
│   └── templates/
│       ├── base.html           # Base template
│       ├── auth.html           # Login/Register
│       ├── dashboard.html      # Main dashboard
│       ├── template_generator.html  # Template creation
│       ├── distribution.html   # Invitation distribution
│       └── settings.html       # User settings
└── .gitignore                  # Git ignore rules
```

## Quick Setup Instructions

### 1. Environment Setup

```bash
# Navigate to backend directory
cd backend

# Copy environment template
cp env.example .env

# Edit .env file with your API keys
# See API_KEYS_DOCUMENTATION.md for details
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Option 1: Use the startup script
python run.py

# Option 2: Run directly
python main.py
```

### 4. Access the Application

- Open your browser and go to: `http://localhost:5001`
- Register a new account or log in
- Start creating AI-powered meeting invitations!

## Environment Variables

Create a `.env` file in the `backend/` directory with:

```env
# Flask Application Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=sqlite:///smartmeeting.db

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
GMAIL_PASSWORD=your-app-password

# WhatsApp Integration (Optional)
WHATSAPP_API_KEY=your-whatsapp-api-key
WHATSAPP_PHONE_NUMBER=your-whatsapp-phone-number

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

## Features Working ✅

- ✅ **User Authentication**: Login/Register system
- ✅ **AI Template Generation**: OpenAI-powered meeting invitations
- ✅ **Gmail Integration**: Send invitations via email
- ✅ **WhatsApp Integration**: Send invitations via WhatsApp
- ✅ **Dashboard Analytics**: Track templates and invitations
- ✅ **Template Management**: Create, save, and download templates
- ✅ **Distribution System**: Send invitations to multiple recipients
- ✅ **Settings Management**: Configure integrations and preferences

## File Organization Benefits

### Backend (`backend/`)
- **Clean Architecture**: Separation of concerns
- **Modular Design**: Each utility has its own file
- **Easy Maintenance**: Business logic is organized
- **Scalability**: Easy to add new features

### Frontend (`frontend/`)
- **Template Organization**: All HTML templates in one place
- **Consistent Design**: Base template ensures uniformity
- **Responsive Design**: Mobile-friendly interface

### Security
- **Environment Variables**: Sensitive data in `.env` files
- **Git Ignore**: Prevents committing sensitive files
- **Input Validation**: Secure form handling

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running from the `backend/` directory
   - Check that all dependencies are installed

2. **Database Issues**
   - The database will be created automatically on first run
   - Check file permissions in the backend directory

3. **Template Not Found**
   - Ensure the `frontend/templates/` directory exists
   - Check the template folder path in `main.py`

4. **API Key Issues**
   - Verify your API keys are correct in `.env`
   - Check the API documentation for setup instructions

### Getting Help

- Check the `API_KEYS_DOCUMENTATION.md` for API setup
- Review the `README.md` for detailed information
- Ensure all files are in the correct directories

## Development

### Adding New Features

1. **Backend Routes**: Add to `main.py`
2. **Business Logic**: Add to appropriate file in `utils/`
3. **Frontend**: Add templates to `frontend/templates/`
4. **Database**: Add models to `utils/models.py`

### Testing

The application is fully functional and ready for use. All core features work as expected:

- User registration and login
- AI-powered template generation
- Email and WhatsApp distribution
- Dashboard analytics
- Settings management

---

**🎉 SmartMeetingAI is now fully functional with the exact structure you specified!** 