from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
    Title=models.CharField(max_length=100)
    Preambule=models.CharField(max_length=100)
    Text=models.CharField(max_length=4000)
    Author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Photo=models.ImageField(upload_to='images')
    Liked=models.IntegerField(default=0, blank=False)
    Disliked=models.IntegerField(default=0, blank=False)
    Created=models.DateTimeField(auto_now_add=True, blank=False)
    Updated = models.DateTimeField(auto_now_add=True)
    Hidden=models.BooleanField(default=False)
    def save(self,*args, **kwargs):
        self.Updated = timezone.now()
        return super().save(*args, **kwargs)

class Message(models.Model):
    Email=models.CharField(max_length=100)
    header=models.CharField(max_length=100)
    Message=models.CharField(max_length=1000)
    Is_replyed=models.BooleanField(default=False)
    Replyed_by=models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, blank=True)
    Reply_header=models.CharField(max_length=200, blank=True)
    Reply_text=models.CharField(max_length=2000, blank=True)