from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_img = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=4096)
    national_id = models.IntegerField()



