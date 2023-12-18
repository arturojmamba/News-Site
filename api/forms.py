from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *


User = get_user_model()

# forms.py

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Enter Email Address')
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'date_of_birth', 'password1', 'password2')
    
    def clean_username(self):
        return self.cleaned_data['email']