import csv
import datetime
import os
from django.apps import apps
from django.core.management.base import  CommandError
from django.db import DataError
from django.conf import settings
from django.core.mail import EmailMessage

# THIS FUNCTIONS ARE KNOWN AS HELPER FUNCTIONS
# FUNCTIONS THAT WE CAN ALL ALONG ALL THE PROJECT

# List all the models that i have created
def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'Upload'] # exclude default models
    
    #try get all apps
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
            
    return custom_models


# Check errors in CSV -> complements task
def check_csv_errors(file_path, model_name):
    # Search for model in all installed apps
    model = None
    
    for app_config in apps.get_app_configs(): # Loops through apps
        # Try to search for the model
        try:
            model = apps.get_model(app_config.label, model_name) # Get Model
            break #stop searching once the model is found
        except LookupError:
            continue # continue searching to another app. Because Model was not found in that app iterated on app_config
        
    if not model:
        raise CommandError(f'Model: {model_name} , not found in any app.')
    
    # get all the field names of the model that we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id'] # exclude id field generated by default
    
    try:
        # WE NEED TO EXCLUDE id because it is put by default from the database but that is not included in our CSV nor in MODELS.
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file) # Considers the first row as CSV header
            csv_header = reader.fieldnames # 
            
        # compare CSV header with model's field names
            if csv_header != model_fields:
                raise DataError(f'CSV file does not match with the {model_name} table fields')
    
    except Exception as e:
        raise e

    return model


def send_mail_notification(mail_subject, message, to_email, attachment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
        if attachment is not None:
            mail.attach_file(attachment)
            
        mail.send()
    except Exception as e:
        raise e
    
    return 'Email sent successfully'

def generate_csv_filepath(model_name):
    # GENERATES FILE NAME and FILE PATH
    
    # generate timestamp of current date and time
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    # folder name to which file will be exported
    export_dir = 'exported_data'
    
    # define the CSV file name
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    
    # join folder and file name
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    
    return file_path