from datetime import date
import logging
from email.mime.text import MIMEText

from src.tasks.email_sender import EmailSender
from src.tasks.celery_app import celery_instance


@celery_instance.task
def send_successful_registration_email_task(new_user_email: str):
    logging.debug("Вызывается функция (celery task) send_successful_registration_email_task")
    message = MIMEText("Здравствуйте!\nВы успешно зарегестрировались в нашем сервисе.")
    message["Subject"] = "Library service notification"

    EmailSender().send_email(recipient_email=new_user_email, message=message)
    logging.info(f"Письмо успешно отправлено на почту: {new_user_email}")


@celery_instance.task
def send_borrow_info_email_task(
    recipient_email: str, date_from: date, date_to: date, book_id: int
) -> None:
    logging.debug("Вызывается функция (celery task) send_borrow_info_email_task")
    message = MIMEText(
        f"Здравствуйте!\nВы взяли книгу (id={book_id}) {date_from}. Просьба вернуть ее {date_to}."
    )
    message["Subject"] = "Library service notification"

    EmailSender().send_email(recipient_email, message)
    logging.info(f"Письмо успешно отправлено на почту: {recipient_email}")
