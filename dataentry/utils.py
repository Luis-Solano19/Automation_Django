import csv
import datetime
import hashlib
import os
import time
from django.apps import apps
from django.core.management.base import  CommandError
from django.db import DataError
from django.conf import settings
from django.core.mail import EmailMessage
from emails.models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup

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


def send_mail_notification(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        
        for recipient_email in to_email:
            new_message = message
            # Create EmailTracking record
            if email_id: # only it it comes from bulky email tool
                email_obj = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list = email_obj.email_list, email_address = recipient_email) # get email subscribed to a specific List
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest() # create unique id
                
                email_tracking = EmailTracking.objects.create(
                    email = email_obj,
                    subscriber = subscriber,
                    unique_id = unique_id
                )
            
                base_url = settings.BASE_URL # domain URL
                
                # Generate the tracking pixel 
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}/" # must be a domain to be publicly accessible
                
                # Open tracking url
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
            
                # Search for the links in the email body
                # We use beautiful soup because the body or message is an HTML because of the ckeditor
                soup = BeautifulSoup(message, 'html.parser')
                
                urls = [a['href'] for a in soup.find_all('a', href=True)] # get all links inside HTML
                
                # If there are links or ulrs in the email body, inject our tracking url to the original link
                if urls:
                    for url in urls:
                        # make the final tracking URL
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")
                else:
                    print('No urls found in the email content')
                
                # Create email content with tracking pixel image outside of if and for because this will detect OPENING of email
                open_tracking_image = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message = new_message + open_tracking_image
                print(f"Final message=>  {new_message}")
            
            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email]) # if not especified like to=[] each email will get the message n times.
            if attachment is not None:
                mail.attach_file(attachment)
        
            mail.content_subtype = "html" # sending content from ckeditor as HTML content so it loads correctly
            mail.send()
        
        # Store the total sent emails inside the Sent Model
        if email_id:
            sent_obj = Sent()
            sent_obj.email = email_obj
            sent_obj.total_sent = email_obj.email_list.count_emails() # Count how many email addresses are linked to a List
            sent_obj.save()
        
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