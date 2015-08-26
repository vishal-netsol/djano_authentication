from django.db import models

class Post(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
  post = models.ForeignKey(Post)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)