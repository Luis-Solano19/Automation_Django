from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# default django forms
from django import forms

class RegistrationForm(UserCreationForm):
    # Fields that are inside the User creation form but not used by default when creating one
    # so we indicate it
    email = forms.EmailField(required=True, label='Email Address')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    