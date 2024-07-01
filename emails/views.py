from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_mail_notification
from django.conf import settings
from .models import Email, Sent, Subscriber, EmailTracking
from .tasks import send_email_task
from django.db.models import Sum
from django.utils import timezone

# Create your views here.


def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email_object = form.save()
            
            # Send an Email.
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            # Access the selected email list
            email_list = email_object.email_list
            
            # Extract email addresses from the subscribers based on relation with List.
            subscribers = Subscriber.objects.filter(email_list=email_list)
            
            to_email = [email.email_address for email in subscribers]
            
            attachment = None
            
            if email_object.attachment:
                attachment = email_object.attachment.path # verify if an attachment was added
            else:
                attachment = None
            
            email_id = email_object.id # recover email id so we can later create the Sent object
            
            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id)
            
            # Display success Message
            messages.success(request, 'Email sent successfully')
            
            return redirect('send_email')
    else:
        form = EmailForm()
        context = {
            'form':form
        }
        return render(request, 'emails/send-email.html', context)
    


def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at') # As if we were asigning total_sent field to Email object
    # the sum() comes from model -> sent__total_sent
    
    context = {
        'emails':emails
    }
    return render(request, 'emails/track_dashboard.html', context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    
    context = {
        'email':email,
        'total_sent':sent.total_sent
    }
    return render(request, 'emails/track_stats.html', context)


# When user clicks on a URL in the email.
def track_click(request, unique_id):
    # to detect clicks we append our domain and unique id to the url:
    # https://domain.com/emails/track/click/uniqueid?url=https://domain.com/link
    # so the request will come first to our server and through that unique id we can obtain info.
    try:
        email_tracking = EmailTracking.objects.get(unique_id = unique_id)
        # because in the tracking link after the ? is a url so is a parameter argument.
        url = request.GET.get('url')
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            
            # We use HttResponseRedirect because it is a server response
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except:
        return HttpResponse('Email click tracking record not found')


# When user opens the email
def track_open(request, unique_id):
    # to track the open rate, we are going to pass our server domain and open view to an img tag.
    # <img src="https://domain.com/emails/track/open/uniqueid/" width=1, height=1>
    # so when user clicks on image, it doesnt display but it triggers the open view.
    # however it is not 100% accurate cuz some email apps auto fetches images to display them so it counts as if they opened it
    # its a common issue, that is why most focus on click rate instead of opening rate
    # Log the request to verify
    try:
        email_tracking = EmailTracking.objects.get(unique_id = unique_id)
        # Check if the opened_at field is already set or no
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse('Email opened successfully')
        else:
            print('Email already opened.')
            return HttpResponse('Email already opened')
    except:
        return HttpResponse('Email tracking record not found')