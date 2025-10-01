import smtplib, logging
import ssl

from email.message import EmailMessage
from app.core.config import EMAIL_CONFIG

def send_email(to_email: str, subject: str, body: str,body_type:str = 'plain'):

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_CONFIG['email']
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body, subtype=body_type)

        context = ssl.create_default_context()

        with  smtplib.SMTP(EMAIL_CONFIG['host'], EMAIL_CONFIG['port']) as server:
            server.starttls(context=context)  # Secure connection
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        logging.info(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        logging.error(f"Error sending email to {to_email} :: {e}")
        return False
