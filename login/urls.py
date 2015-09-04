from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
  url(r'^register/$', views.register, name="register"),
  url(r'^create/$', views.create, name="create"),
  url(r'^login/$', views.login, name="login"),
  url(r'^logout/$', views.logout, name="logout"),
  url(r'^authenticate/$', views.authenticate, name="authenticate"),
  #api-token
  url(r'^api-token-auth/', rest_views.obtain_auth_token)

]