from django.db import models


class Offer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    offer_price = models.IntegerField()
    offer_date = models.DateField()
    offer_expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),('contingent', 'Contingent'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')



