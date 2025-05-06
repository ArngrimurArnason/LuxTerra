from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_img = models.CharField(max_length=4096)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=4096)
    national_id = models.IntegerField()



