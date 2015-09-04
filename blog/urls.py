"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from login.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>\d+)/$', views.show, name="show"),
    url(r'^post/new', views.new, name="new"),
    url(r'^post/create', views.create, name="create"),
    url(r'^post/(?P<post_id>\d+)/comments', views.add_comments, name="add_comments"),
    url(r'^post/(?P<post_id>\d+)/delete', views.delete, name="delete"),
    url(r'^post/(?P<post_id>\d+)/edit', views.edit, name="edit"),
    url(r'^post/(?P<post_id>\d+)/update', views.update, name="update"),
    url(r'^users/', include('login.urls', namespace="users")),
    #api
    url(r'^api/v1/posts/$', views.PostCollection.as_view()),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)$', views.PostMember.as_view())

]
