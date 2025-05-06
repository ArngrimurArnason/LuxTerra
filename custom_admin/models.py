from django.db import models
class Custom_Admin(models.Model):
    adminid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

