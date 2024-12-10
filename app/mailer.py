import smtplib
from email.mime.text import MIMEText
from app.logger import logger
import os

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(to_email: str, subject: str, body: str) -> bool:


    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)

            msg = MIMEText(body)
            msg["From"] = SMTP_USER
            msg["To"] = to_email


            server.sendmail(SMTP_USER, to_email, msg.as_string())
            logger.info(f"Email sent to {to_email}: {subject}")

            server.quit()
            return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False