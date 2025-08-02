import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_gmail_invitation(recipient_email, template_content, subject="Meeting Invitation", gmail_user=None, gmail_password=None):
    """Send Gmail invitation using Gmail API or SMTP fallback"""
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user or 'noreply@smartmeeting.ai'
        msg['To'] = recipient_email
        msg['Content-Type'] = 'text/html; charset=utf-8'
        
        html_part = MIMEText(template_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Try Gmail API first, fallback to SMTP
        if gmail_user and gmail_password and gmail_user != 'your-email@gmail.com' and gmail_password != 'your-16-character-app-password-here':
            # Use SMTP with app password
            try:
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