from django.core.management.base import BaseCommand


# Proposed command = python manage.py greeting Username
# proposed output = Hi, {Username}, have a good day!
class Command(BaseCommand):
    help = "This greets the user"
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Specifies user name')
    
    def handle(self, *args, **kwargs):
        username = kwargs['username']
        greeting = f"Hi {username}, have a good day!"
        self.stdout.write(self.style.SUCCESS(greeting))
        # self.stdout.write(self.style.WARNING(greeting))
        # self.stderr.write(greeting) # prints an error or color red