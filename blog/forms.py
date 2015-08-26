from django import forms
from django.forms import ModelForm
from .models import *

class PostForm(forms.Form):
  title = forms.CharField(max_length=100)
  content = forms.CharField(widget=forms.Textarea)

class FieldPostForm(ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'content']