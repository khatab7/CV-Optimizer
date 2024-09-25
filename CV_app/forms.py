from django import forms
from .models import CV
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['name', 'email', 'phone', 'skills', 'experience', 'education']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
