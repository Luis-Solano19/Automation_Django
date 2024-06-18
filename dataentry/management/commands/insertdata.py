from django.core.management.base import BaseCommand
from dataentry.models import Student

# I wish to add some data to my database using the custom command

class Command(BaseCommand):
    help = ""
    
    def handle(self, *args, **kwargs):
        # logic goes here.
        # add 1 record
        # Student.objects.create(roll_no = 1001, name = 'Luis', age = 25) # inserts data
        
        dataset = [
            {'roll_no':1002, 'name':'Sohee', 'age':26},
            {'roll_no':1003, 'name':'Maki', 'age':28},
            {'roll_no':1005, 'name':'JU', 'age':18},
            {'roll_no':1006, 'name':'Mili', 'age':15},
            {'roll_no':1007, 'name':'Leilani', 'age':21},
        ]
        
        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no = roll_no).exists()
            if not existing_record:
                Student.objects.create(roll_no = data['roll_no'], name=data['name'], age=data['age'])
                self.stdout.write(self.style.SUCCESS("Data inserted successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Data with roll_no {roll_no} already exists. "))
