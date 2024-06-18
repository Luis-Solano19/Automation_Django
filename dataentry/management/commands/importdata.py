from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import csv

# PROPOSED COMMAND - python manage.py impordata - filepath modelname

class Command(BaseCommand):
    help = "This imports data from CSV file"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Indicates the path to the CSV file.')
        parser.add_argument('model_name', type=str, help='Indicates the name of the Model')
    
    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        
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
        
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        
        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully"))
        
        
        
        
# For just one MODEL:


# class Command(BaseCommand):
#     help = "This imports data from CSV file"
    
#     def add_arguments(self, parser):
#         parser.add_argument('file_path', type=str, help='Indicates the path to the CSV file.')
    
#     def handle(self, *args, **kwargs):
#         # logic goes here
#         file_path = kwargs['file_path']
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 roll_no = row['roll_no']
#                 # Student.objects.create(roll_no = row['roll_no'], name=row['name'], age=row['age']) instead we can do:
#                 # **row will match every value on dictionaries with database columns but the CSV has to be matched in columns
#                 existing_roll_no = Student.objects.filter(roll_no = roll_no).exists()
#                 if not existing_roll_no:
#                     Student.objects.create(**row)
#                 else:
#                     self.stdout.write(self.style.WARNING(f"Data with roll_no: {roll_no} already exists."))
        
#         self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully"))
            
        
