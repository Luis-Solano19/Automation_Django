from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import generate_csv_filepath, send_mail_notification
from django.conf import settings

# tasks for celery

@app.task # celery task
def celery_test_task():
    time.sleep(10)
    # send and email
    mail_subject = 'Test oli'
    message = 'Olix2'
    to_email = settings.DEFAULT_TO_EMAIL
    send_mail_notification(mail_subject, message, to_email)
    return 'Email sent successfully'

@app.task
def import_data_task(absolute_file_path, model_name):
    try:
        call_command('importdata', absolute_file_path, model_name) # importdata command created before
    except Exception as e:
        raise e
    
    # Notify user by email
    mail_subject = f'Import data to model: - {model_name} - completed.'
    message = 'You data import finished.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_mail_notification(mail_subject, message, to_email)
    
    return 'Data imported successfully'


@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    
    # GET WHERE THE FILE WAS GENRATED
    file_path = generate_csv_filepath(model_name)
    
    # Send email with attachement.
    mail_subject = 'Export Data Successful'
    message = 'Export data successful, please download the attachment'
    to_email = settings.DEFAULT_TO_EMAIL
    
    send_mail_notification(mail_subject, message, to_email, attachment=file_path)
    
    return 'Export Data task executed successfully'