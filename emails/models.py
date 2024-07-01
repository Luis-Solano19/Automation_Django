from django.db import models
from ckeditor.fields import RichTextField # From ckeditor

# Create your models here.

class List(models.Model):
    email_list = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.email_list
    
    def count_emails(self):
        count = Subscriber.objects.filter(email_list = self).count() # return the amount of emails that received an email aka count of emails register to a List
        return count
 
   
class Subscriber(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=100)
    
    def __str__(self) -> str:
        return self.email_address
    
    
class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = RichTextField()
    attachment = models.FileField(upload_to='email_attachments/', blank=True) # blank because it can be optional
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.subject
    
    def open_rate(self):
        total_sent = self.email_list.count_emails()
        opened_count = EmailTracking.objects.filter(email = self, opened_at__isnull=False).count() # Filter by email, get all, and then count. 
        # opened_at__isnull must be False so we know the email was already opened.
        # Formula
        open_rate = (opened_count/total_sent) * 100 if total_sent > 0 else 0
        return round(open_rate)
    
    def click_rate(self):
        total_sent = self.email_list.count_emails()
        opened_count = EmailTracking.objects.filter(email = self, opened_at__isnull=False).count() # Filter by email, get all, and then count. 
        
        if opened_count > 0:
            clicked_count = EmailTracking.objects.filter(email = self, clicked_at__isnull=False).count()
            click_rate = (clicked_count/opened_count) * 100 if total_sent > 0 else 0
        else:
            click_rate = 0
        
        return round(click_rate, 2)
        
 

class Sent(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    total_sent = models.IntegerField()  # get the amount of emails registered to a LIST.
    
    def __str__(self) -> str:
        return f"{self.email.subject} - {self.total_sent} emails sent" # it will be like: email subject - 3 emails sent
    

class EmailTracking(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, null=True, blank=True)
    unique_id = models.CharField(max_length=255, unique=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.email.subject