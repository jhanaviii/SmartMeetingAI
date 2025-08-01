# Gmail Integration Setup Guide

## Overview
SmartMeetingAI now supports real Gmail integration for sending beautiful meeting invitations directly to your recipients.

## Setup Options

### Option 1: Gmail App Password (Recommended - Easy Setup)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Navigate to Security → 2-Step Verification → App passwords
   - Select "Mail" and generate a password
3. **Configure Environment Variables**:
   ```env
   GMAIL_USER=your-email@gmail.com
   GMAIL_PASSWORD=your-16-character-app-password
   ```

### Option 2: Gmail API (Advanced - More Features)

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
2. **Enable Gmail API**:
   - Go to APIs & Services → Library
   - Search for "Gmail API" and enable it
3. **Create Credentials**:
   - Go to APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Download the JSON credentials file
4. **Configure Environment Variables**:
   ```env
   GMAIL_USER=your-email@gmail.com
   GMAIL_CREDENTIALS_FILE=path/to/credentials.json
   ```

## Environment Configuration

Update your `.env` file with the following:

```env
# Gmail Integration
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password

# Optional: For Gmail API
GMAIL_CREDENTIALS_FILE=credentials.json
```

## Features

### ✅ What's Working Now:
- **Multiple Recipients**: Send to multiple email addresses at once
- **Beautiful Templates**: Your AI-generated templates are sent as HTML emails
- **Custom Subjects**: Personalized subject lines with meeting topics
- **Preview Function**: Preview templates before sending
- **Send Tracking**: Track successful and failed sends
- **Fallback Mode**: Works in demo mode if credentials aren't configured

### 🎯 How to Use:

1. **Create a Template**: Use the Template Generator to create your meeting invitation
2. **Go to Distribution**: Navigate to the Distribution page
3. **Select Template**: Choose the template you want to send
4. **Enter Recipients**: Add one or multiple email addresses (one per line)
5. **Customize Subject**: Edit the subject line if needed
6. **Preview**: Click "Preview" to see how the email will look
7. **Send**: Click "Send via Gmail" to send the invitations

### 📧 Email Features:
- **HTML Formatting**: Beautiful, responsive email templates
- **Professional Styling**: Gradients, cards, icons, and modern design
- **Mobile Responsive**: Looks great on all devices
- **Branding**: SmartMeetingAI branding included

## Troubleshooting

### Common Issues:

1. **"Authentication failed"**:
   - Check your Gmail credentials
   - Ensure 2FA is enabled and app password is correct
   - Verify Gmail account settings allow "less secure apps"

2. **"Demo mode" message**:
   - Configure Gmail credentials in your `.env` file
   - Restart the application after configuration

3. **"Invalid email format"**:
   - Check email addresses for typos
   - Ensure proper email format (user@domain.com)

### Security Notes:
- Never commit your `.env` file to version control
- Use app passwords instead of your main Gmail password
- Regularly rotate your app passwords

## Demo Mode

If Gmail credentials aren't configured, the system runs in demo mode:
- Shows success messages but doesn't actually send emails
- Perfect for testing the interface
- Configure credentials to enable real sending

## Next Steps

1. **Configure Gmail credentials** in your `.env` file
2. **Test with a single recipient** first
3. **Try multiple recipients** for batch sending
4. **Use the preview function** to check your templates
5. **Monitor send status** in the distribution history

Your SmartMeetingAI is now ready for professional email distribution! 🎉 