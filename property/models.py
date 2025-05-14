from django.db import models


class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    admin_approval = models.BooleanField(default=False)
    street =    models.CharField(max_length=100)
    house_number = models.IntegerField()
    city = models.CharField(max_length=100)
    post_code = models.IntegerField(max_length=3, choices=[
        '101','102','103','104','105','106','107','108','109',
        '110','111','112','113','116','161','162','170','200',
        '201','202','203','206','210','212','225','220','221',
        '222','230','232','240','241','270','271','276','300',
        '400','401','550','600','601','602','700','735','736',
        '800','801','870','871','900','901',
    ])
    property_type = models.CharField(max_length=50, choices=[
        'Apartment',
        'House',
        'Bungalow',
        'Villa',
        'Penthouse'
    ])
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




