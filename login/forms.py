from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password']

class LoginForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'password']