import csv
from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
import datetime
from django.apps import apps

from dataentry.utils import generate_csv_filepath

# proposed command = python manage.py exportdata model_name

class Command(BaseCommand):
    help = "This command exports data from a database/model to a CSV file. "
    
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Indicates the name of the model/database from which to export data')
    
    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()
        
        #search for model
        model = None
        
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue
        
        if not model:
            self.stderr.write(f'Model: {model_name}, not found in any apps.')
            return

        # fetch the data from the database
        data = model.objects.all()
        
        # generate CSV file path
        file_path = generate_csv_filepath(model_name)

        # open the CSV file and then write the data and save it in FILE_PATH indicated
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # write the CSV header
            # print the field names of the model that we want to export
            writer.writerow([field.name for field in model._meta.fields])
            
            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
        
        
        self.stdout.write(self.style.SUCCESS('Data exported successfully '))
        



# Export data from multiple tables
# class Command(BaseCommand):
#     help = "This command exports data from a database/model to a CSV file. "
    
#     def add_arguments(self, parser):
#         parser.add_argument('model_name', type=str, help='Indicates the name of the model/database from which to export data')
    
#     def handle(self, *args, **kwargs):
#         model_name = kwargs['model_name'].capitalize()
        
#         #search for model
#         model = None
        
#         for app_config in apps.get_app_configs():
#             try:
#                 model = apps.get_model(app_config.label, model_name)
#                 break
#             except LookupError:
#                 continue
        
#         if not model:
#             self.stderr.write(f'Model: {model_name}, not found in any apps.')
#             return

#         # fetch the data from the database
#         data = model.objects.all()
        
#         # generate timestamp of current date and time
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
#         # define the CSV file name/path
#         file_path = f'exported_{model_name}_data_{timestamp}.csv'

#         # open the CSV file and then write the data
#         with open(file_path, 'w', newline='') as file:
#             writer = csv.writer(file)
            
#             # write the CSV header
#             # print the field names of the model that we want to export
#             writer.writerow([field.name for field in model._meta.fields])
            
#             # write data rows
#             for dt in data:
#                 writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
        
        
#         self.stdout.write(self.style.SUCCESS('Data exported successfully '))

# Export data from single table

# class Command(BaseCommand):
#     help = "This command exports data from a database / model to a CSV file. "
    
#     def handle(self, *args, **kwargs):
#         # fetch the data from the database
#         students = Student.objects.all()
        
#         # generate timestamp of current date and time
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
#         # define the CSV file name/path
#         file_path = f'exported_students_data_{timestamp}.csv'

#         # open the CSV file and then write the data
#         with open(file_path, 'w', newline='') as file:
#             writer = csv.writer(file)
            
#             # write the CSV header
#             writer.writerow(['Roll No', 'Name', 'Age'])
            
#             # write data rows
#             for student in students:
#                 writer.writerow([student.roll_no, student.name, student.age])
        
        
#         self.stdout.write(self.style.SUCCESS('Data exported successfully '))