from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as user_logout
from django.contrib.auth import authenticate as auth, login as user_login
from django.contrib.auth.forms import *

# Create your views here.
def register(request):
  form = UserCreationForm()
  return render(request, 'users/register.html', {'form': form})

def create(request):
  form = UserCreationForm(request.POST)
  if form.is_valid():
    form.save()
    return HttpResponseRedirect('/')
  else:
    return render(request, 'users/register.html', {'form': form})

def login(request):
  form = AuthenticationForm()
  return render(request, 'users/login.html', {'form': form})

def logout(request):
  user_logout(request)
  return HttpResponseRedirect('/users/login')

def authenticate(request):
  print request.POST['username']
  user = auth(username=request.POST['username'], password=request.POST['password'])
  print user
  if user is not None:
    user_login(request, user)
    return HttpResponseRedirect('/')
  else:
    return HttpResponseRedirect('/users/login')
