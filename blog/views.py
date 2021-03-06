from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import mixins, generics
from django.views.generic.detail import *
import pdb
from rest_framework.authentication import *
from rest_framework.permissions import IsAuthenticated

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



class PostCollection(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):

  queryset = Post.objects.all()
  serializer_class = PostSerializer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

#@api_view(['GET', 'POST'])
# def post_collection(request):
#   if request.method == "GET":
#     posts = Post.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)
#   elif request.method == 'POST':
#     data = {'title': request.data['post']['title'], 'content': request.data['post']['content']}
#     serializer = PostSerializer(data=data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)

class PostMember(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  generics.GenericAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer

  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    #pdb.set_trace()
    #kwargs['partial'] = True
    return self.partial_update(request, *args, **kwargs)


# @api_view(['GET', 'DELETE', 'PUT'])
# def post_element(request, pk):
#   post = get_object_or_404(Post, id=pk)
#   if request.method == 'GET':
#     return Response(PostSerializer(post).data)
#   elif request.method == 'DELETE':
#     post.delete()
#     return Response("Post successfully deleted")
#   elif request.method == 'PUT':
#     serializer = PostSerializer(post, data=request.data['post'], partial=True)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors)