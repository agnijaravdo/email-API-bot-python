import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_an_email(email, newsletter_message):

    msg = EmailMessage()
    msg["Subject"] = "Your daily newsletter!"
    msg["From"] = email
    msg["To"] = email
    msg.set_content(newsletter_message, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(email, os.getenv("APP_PASSWORD"))
            s.send_message(msg)
            return "Email sent successfully!"
    except smtplib.SMTPAuthenticationError as e:
        return f"Email Authentication failed: {e}"
    except smtplib.SMTPException as e:
        return f"An SMTP error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"
