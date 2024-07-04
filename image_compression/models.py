from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CompressImage(models.Model):
    # like (10,10), (20,20) because in the select tag in HTML we need to provide value="" and the Value displayed in text.
    QUALITY_CHOICES = [(i,i) for i in range(10, 101, 10)] 
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    original_img = models.ImageField(upload_to='original_images/')
    quality = models.IntegerField(choices=QUALITY_CHOICES, default=80)
    compressed_img = models.ImageField(upload_to='compressed_images/')
    compressed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.username