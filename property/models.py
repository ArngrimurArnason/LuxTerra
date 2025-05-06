from django.db import models
from user.models import User

class Property(models.Model):
    propertyid = models.AutoField(primary_key=True)
    userid = models.ForeignKey('user.User', on_delete=models.CASCADE)
    admin_approval = models.BooleanField(default=False)
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()
    city = models.CharField(max_length=100)
    post_code = models.IntegerField()
    property_type = models.CharField(max_length=100)
    price = models.IntegerField()
    build_date = models.DateField()
    description = models.CharField(max_length=4096)
    bathroom = models.IntegerField()
    bedrooms = models.IntegerField()
    size = models.IntegerField()
    property_status = models.BooleanField()

class PropertyImages(models.Model):
    images = models.CharField(max_length=4096)
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE)
