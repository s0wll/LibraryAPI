import smtplib

from src.tasks.config import sender_email, sender_password


class EmailSender:
    def send_email(recipient_email: str, message: str) -> None:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
