from django.db import models
from user.models import User
from property.models import Property
class Offer(models.Model):
    offerid = models.AutoField(primary_key=True)
    userid = models.ForeignKey('user.User', on_delete=models.CASCADE)
    propertyid = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    offer_price = models.IntegerField()
    offer_date = models.DateField()
    offer_expiry_date = models.DateField()



