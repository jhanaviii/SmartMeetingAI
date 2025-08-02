import openai
import os
from flask import current_app

def generate_template_content_with_openai(meeting_data, openai_api_key):
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
            client = openai.OpenAI(api_key=openai_api_key)
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
                    
                    <!-- Content -->
                    <div style="padding: 40px 30px;">
                        <h2 style="margin: 0 0 30px 0; font-size: 28px; color: #2c3e50; text-align: center;">{meeting_data.get('meetingTopic', 'Meeting')}</h2>
                        
                        <!-- Priority Badge -->
                        <div style="text-align: center; margin-bottom: 30px;">
                            <span style="background: {priority_bg}; color: {priority_color}; padding: 8px 20px; border-radius: 25px; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; border: 2px solid {priority_color};">
                                {meeting_data.get('priority', 'Medium')} Priority
                            </span>
                        </div>
                        
                        <!-- Meeting Details -->
                        <div style="background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;">
                            <h3 style="margin: 0 0 20px 0; color: #667eea; font-size: 20px; display: flex; align-items: center;">
                                <span style="margin-right: 10px;">📋</span> Meeting Details
                            </h3>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                <div style="background: white; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                                    <div style="font-weight: 600; color: #667eea; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">📅 Date</div>
                                    <div style="color: #2c3e50; font-size: 16px; margin-top: 5px;">{meeting_data.get('date', 'TBD')}</div>
                                </div>
                                
                                <div style="background: white; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                                    <div style="font-weight: 600; color: #667eea; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">🕐 Time</div>
                                    <div style="color: #2c3e50; font-size: 16px; margin-top: 5px;">{meeting_data.get('time', 'TBD')}</div>
                                </div>
                                
                                <div style="background: white; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                                    <div style="font-weight: 600; color: #667eea; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">⏱️ Duration</div>
                                    <div style="color: #2c3e50; font-size: 16px; margin-top: 5px;">{meeting_data.get('duration', 'TBD')}</div>
                                </div>
                                
                                <div style="background: white; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                                    <div style="font-weight: 600; color: #667eea; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">🎤 Speaker</div>
                                    <div style="color: #2c3e50; font-size: 16px; margin-top: 5px;">{meeting_data.get('speakerName', 'TBD')}</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Location -->
                        {f'<div style="background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;"><h3 style="margin: 0 0 15px 0; color: #667eea; font-size: 20px; display: flex; align-items: center;"><span style="margin-right: 10px;">📍</span> Location</h3><p style="margin: 0; color: #2c3e50; font-size: 16px;">{meeting_data.get("location", "")}</p></div>' if meeting_data.get('location') else ''}
                        
                        <!-- Meeting Link -->
                        {f'<div style="background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;"><h3 style="margin: 0 0 15px 0; color: #667eea; font-size: 20px; display: flex; align-items: center;"><span style="margin-right: 10px;">🔗</span> Meeting Link</h3><p style="margin: 0;"><a href="{meeting_data.get("meetingLink", "")}" style="color: #667eea; text-decoration: none; font-weight: 600; background: white; padding: 10px 20px; border-radius: 8px; display: inline-block;">Join Meeting</a></p></div>' if meeting_data.get('meetingLink') else ''}
                        
                        <!-- Agenda -->
                        {f'<div style="background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;"><h3 style="margin: 0 0 15px 0; color: #667eea; font-size: 20px; display: flex; align-items: center;"><span style="margin-right: 10px;">📋</span> Agenda</h3><p style="margin: 0; color: #2c3e50; font-size: 16px;">{meeting_data.get("agenda", "")}</p></div>' if meeting_data.get('agenda') else ''}
                        
                        <!-- Attendees -->
                        {f'<div style="background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;"><h3 style="margin: 0 0 15px 0; color: #667eea; font-size: 20px; display: flex; align-items: center;"><span style="margin-right: 10px;">👥</span> Attendees</h3><p style="margin: 0; color: #2c3e50; font-size: 16px;">{", ".join(meeting_data.get("attendees", []))}</p></div>' if meeting_data.get('attendees') else ''}
                        
                        <!-- Additional Notes -->
                        {f'<div style="background: #f8f9fa; border-radius: 15px; padding: 25px; margin-bottom: 25px;"><h3 style="margin: 0 0 15px 0; color: #667eea; font-size: 20px; display: flex; align-items: center;"><span style="margin-right: 10px;">📝</span> Additional Notes</h3><p style="margin: 0; color: #2c3e50; font-size: 16px;">{meeting_data.get("additionalNotes", "")}</p></div>' if meeting_data.get('additionalNotes') else ''}
                        
                        <!-- Call to Action -->
                        <div style="text-align: center; margin: 40px 0;">
                            <a href="#" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: 600; font-size: 16px; display: inline-block; box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3); transition: all 0.3s ease;">Confirm Attendance</a>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background: #2c3e50; color: white; padding: 30px; text-align: center;">
                        <p style="margin: 0; font-size: 14px; opacity: 0.8;">Generated by SmartMeetingAI • Professional Meeting Coordination</p>
                        <p style="margin: 10px 0 0 0; font-size: 12px; opacity: 0.6;">Please respond to confirm your attendance</p>
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