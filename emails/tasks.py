from awd_main.celery import app
from dataentry.utils import send_mail_notification


@app.task
def send_email_task(mail_subject, message, to_email, attachment):
    try:
        send_mail_notification(mail_subject, message, to_email, attachment)
    except Exception as e:
        raise e
    
    return 'Email from task sent successfully'