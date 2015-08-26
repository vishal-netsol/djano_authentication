from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/login/')
def new(request):
  form = FieldPostForm()
  return render(request, 'blog/new.html', {'form': form})

@login_required(login_url='/users/login/')
def index(request):
  posts = Post.objects.all()
  return render(request, 'blog/index.html', {'posts': posts})

@login_required(login_url='/users/login/')
def show(request, post_id):
  try:
    post = get_object_or_404(Post, pk=post_id)
  except Post.DoesNotExist:
    raise Http404("Post Not Found")
  return render(request, 'blog/show.html', {'post': post})

@login_required(login_url='/users/login/')
def create(request):
  post = Post.objects.create(title=request.POST['title'], content=request.POST['content'],
      created_at=datetime.utcnow())
  return HttpResponseRedirect(reverse('show', kwargs={'post_id':post.id}))

@login_required(login_url='/users/login/')
def add_comments(request, post_id):
  try:
    post = get_object_or_404(Post, pk=post_id)
    post.comment_set.create(message=request.POST['message'], created_at=datetime.utcnow())
  except Post.DoesNotExist:
    raise Http404("Post Not Found")
  return HttpResponseRedirect(reverse('show', kwargs={'post_id':post.id}))

@login_required(login_url='/users/login/')
def delete(request, post_id):
  try:
    post = get_object_or_404(Post, pk=post_id)
    post.comment_set.all().delete()
    post.delete()
  except Post.DoesNotExist:
    raise Http404("Post Not Found")
  return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/users/login/')
def edit(request, post_id):
  try:
    post = get_object_or_404(Post, pk=post_id)
    form = FieldPostForm(instance=post)
  except Post.DoesNotExist:
    raise Http404("Post Not Found")
  return render(request, 'blog/edit.html', {'post': post, 'form': form})

@login_required(login_url='/users/login/')
def update(request, post_id):
  try:
    post = get_object_or_404(Post, pk=post_id)
    form = FieldPostForm(request.POST, instance=post)
    form.save()
  except Post.DoesNotExist:
    raise Http404("Post Not Found")
  return HttpResponseRedirect(reverse(show, kwargs={'post_id': post.id}))