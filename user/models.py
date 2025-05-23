from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    profile_img = models.ImageField(upload_to='profile_img', blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    national_id = models.CharField(max_length=10)

    def __str__(self):
        return self.username



