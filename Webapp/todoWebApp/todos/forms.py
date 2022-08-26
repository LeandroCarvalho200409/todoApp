from django import forms
from django.forms import ModelForm
from .models import todo
from .views import *
from .widget import DatePickerInput

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField()

class TodoForm(forms.Form):
    name = forms.CharField()
    text = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(widget=DatePickerInput())
    done = forms.BooleanField(required=False)

    
