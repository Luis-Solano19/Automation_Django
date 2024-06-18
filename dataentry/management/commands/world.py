from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This prints a hello world."

    def handle(self, *args, **kwargs):
        # we write the logic
        self.stdout.write("Hello world")