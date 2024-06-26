from django.shortcuts import redirect, render
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_mail_notification
from django.conf import settings
from .models import Subscriber
from .tasks import send_email_task

# Create your views here.


def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()
            # Send an Email.
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            # Access the selected email list
            email_list = form.email_list
            
            # Extract email addresses from the subscribers based on relation with List.
            subscribers = Subscriber.objects.filter(email_list=email_list)
            
            to_email = [email.email_address for email in subscribers]
            
            attachment = None
            
            if form.attachment:
                attachment = form.attachment.path
            else:
                attachment = None
            
            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)
            
            # Display success Message
            messages.success(request, 'Email sent successfully')
            
            return redirect('send_email')
    else:
        form = EmailForm()
        context = {
            'form':form
        }
        return render(request, 'emails/send-email.html', context)