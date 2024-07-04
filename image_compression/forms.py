from django import forms
from .models import CompressImage

class CompressImageForm(forms.ModelForm):
    class Meta:
        model = CompressImage
        fields = ('original_img', 'quality',)
    
    # Change label's name.
    original_img = forms.ImageField(label='Upload an Image')