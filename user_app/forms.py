from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, label='Код подтверждения')


