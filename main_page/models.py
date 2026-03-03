from django.db import models
from django.utils import timezone




class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150,blank=True)
    last_name = models.CharField(max_length=150,blank=True)
    middle_name = models.CharField(max_length=150,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20,blank=True)
    password = models.CharField()




