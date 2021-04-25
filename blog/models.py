from django.contrib.auth.models import User, UserManager, AbstractUser
from django.db import models


class Profile(models.Model):
    mobile = models.IntegerField()
    profession = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)