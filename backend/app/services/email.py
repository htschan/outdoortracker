from flask import current_app, request
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, html_content):
    """Send an email with the configured mail server"""
    try:
        # Get mail configuration
        mail_server = current_app.config['MAIL_SERVER']
        mail_port = current_app.config['MAIL_PORT']
        mail_use_tls = current_app.config['MAIL_USE_TLS']
        mail_username = current_app.config['MAIL_USERNAME']
        mail_password = current_app.config['MAIL_PASSWORD']
        mail_sender = current_app.config['MAIL_DEFAULT_SENDER']
        debug_email = current_app.config.get('DEBUG_EMAIL', False)
        
        # Log diagnostic info when debug_email is enabled
        if debug_email:
            print("\n----- EMAIL DEBUG INFORMATION -----")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Sending email to: {to_email}")
            print(f"Subject: {subject}")
            print(f"From: {mail_sender}")
            print(f"Mail Server: {mail_server}")
            print(f"Mail Port: {mail_port}")
            print(f"Use TLS: {mail_use_tls}")
            print(f"Mail Username: {mail_username}")
            print("Mail Password: [REDACTED]")
            print("----------------------------------\n")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = mail_sender
        msg['To'] = to_email
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to server and send
        server = smtplib.SMTP(mail_server, mail_port)
        if mail_use_tls:
            server.starttls()
        
        if mail_username and mail_password:
            server.login(mail_username, mail_password)
            
        server.sendmail(mail_sender, to_email, msg.as_string())
        server.quit()
        
        # Log success if debug_email is enabled
        if current_app.config.get('DEBUG_EMAIL', False):
            print("\n----- EMAIL SENT SUCCESSFULLY -----")
            print(f"Recipient: {to_email}")
            print("----------------------------------\n")
        
        return True
    
    except Exception as e:
        debug_email = current_app.config.get('DEBUG_EMAIL', False)
        
        # Enhanced error logging with debug_email
        if debug_email:
            print("\n----- EMAIL ERROR DETAILS -----")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"Recipient: {to_email}")
            print(f"Server: {mail_server}:{mail_port}")
            print(f"TLS: {mail_use_tls}")
            print(f"Username provided: {'Yes' if mail_username else 'No'}")
            print(f"Password provided: {'Yes' if mail_password else 'No'}")
            print("------------------------------\n")
        else:
            # Basic error logging
            print(f"Email sending failed: {str(e)}")
        
        # In production, this should be logged properly
        if not current_app.debug:
            current_app.logger.error(f"Email sending failed: {str(e)}")
            
        return False


def send_verification_email(to_email, token):
    """Send email verification link"""
    # In a real app, we would use a proper frontend URL
    verification_url = f"{request.host_url.rstrip('/')}/verify-email/{token}"
    
    # Log verification details if debug_email is enabled
    if current_app.config.get('DEBUG_EMAIL', False):
        print("\n----- VERIFICATION EMAIL DEBUG -----")
        print(f"Token generated: {token}")
        print(f"Verification URL: {verification_url}")
        print("----------------------------------\n")
    
    subject = "Outdoor Tracker: Verify Your Email Address"
    
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .button {{ display: inline-block; padding: 10px 20px; background-color: #4DBA87; color: white; 
                          text-decoration: none; border-radius: 5px; }}
                .footer {{ margin-top: 40px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Verify Your Email Address</h2>
                <p>Thank you for registering with Outdoor Tracker. Please click the button below to verify your email address:</p>
                <p><a href="{verification_url}" class="button">Verify Email Address</a></p>
                <p>If you didn't request this email, you can safely ignore it.</p>
                <p>This link will expire in 24 hours.</p>
                <div class="footer">
                    <p>Outdoor Tracker Team</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(to_email, subject, html_content)
