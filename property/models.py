from django.db import models


class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    admin_approval = models.BooleanField(default=False)
    street =    models.CharField(max_length=100)
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
    thumbnail = models.ImageField(upload_to='property_thumbnails/', blank=True, null=True)

def __str__(self):
    return f"{self.street} {self.house_number} - {self.city}"


class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')


