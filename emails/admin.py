from django.contrib import admin
from .models import List, Subscriber, Email, EmailTracking, Sent
# Register your models here.


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'email_list')

class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscriber', 'opened_at', 'clicked_at')

admin.site.register(List)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Email)
admin.site.register(EmailTracking, EmailTrackingAdmin)
admin.site.register(Sent)