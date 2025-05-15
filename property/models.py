from django.db import models
LOCATION_CHOICES = [
    ('101 - Reykjavík', '101 - Reykjavík'),
    ('102 - Reykjavík', '102 - Reykjavík'),
    ('103 - Reykjavík', '103 - Reykjavík'),
    ('104 - Reykjavík', '104 - Reykjavík'),
    ('105 - Reykjavík', '105 - Reykjavík'),
    ('106 - Reykjavík', '106 - Reykjavík'),
    ('107 - Reykjavík', '107 - Reykjavík'),
    ('108 - Reykjavík', '108 - Reykjavík'),
    ('109 - Reykjavík', '109 - Reykjavík'),
    ('110 - Reykjavík', '110 - Reykjavík'),
    ('111 - Reykjavík', '111 - Reykjavík'),
    ('112 - Reykjavík', '112 - Reykjavík'),
    ('113 - Reykjavík', '113 - Reykjavík'),
    ('116 - Reykjavík', '116 - Reykjavík'),
    ('161 - Reykjavík', '161 - Reykjavík'),
    ('162 - Reykjavík', '162 - Reykjavík'),
    ('170 - Seltjarnarnes', '170 - Seltjarnarnes'),
    ('200 - Kópavogur', '200 - Kópavogur'),
    ('201 - Kópavogur', '201 - Kópavogur'),
    ('202 - Kópavogur', '202 - Kópavogur'),
    ('203 - Kópavogur', '203 - Kópavogur'),
    ('206 - Kópavogur', '206 - Kópavogur'),
    ('210 - Garðabær', '210 - Garðabær'),
    ('212 - Garðabær', '212 - Garðabær'),
    ('225 - Garðabær', '225 - Garðabær'),
    ('220 - Hafnafjörður', '220 - Hafnafjörður'),
    ('221 - Hafnafjörður', '221 - Hafnafjörður'),
    ('222 - Hafnafjörður', '222 - Hafnafjörður'),
    ('230 - Keflavík', '230 - Keflavík'),
    ('232 - Keflavík', '232 - Keflavík'),
    ('240 - Grindavík', '240 - Grindavík'),
    ('241 - Grindavík', '241 - Grindavík'),
    ('270 - Mosfellsbær', '270 - Mosfellsbær'),
    ('271 - Mosfellsbær', '271 - Mosfellsbær'),
    ('276 - Mosfellsbær', '276 - Mosfellsbær'),
    ('300 - Akranes', '300 - Akranes'),
    ('400 - Ísafjörður', '400 - Ísafjörður'),
    ('401 - Ísafjörður', '401 - Ísafjörður'),
    ('550 - Sauðárkrókur', '550 - Sauðárkrókur'),
    ('600 - Akureyri', '600 - Akureyri'),
    ('601 - Akureyri', '601 - Akureyri'),
    ('602 - Akureyri', '602 - Akureyri'),
    ('700 - Egilsstaðir', '700 - Egilsstaðir'),
    ('735 - Eskifjörður', '735 - Eskifjörður'),
    ('736 - Eskifjörður', '736 - Eskifjörður'),
    ('800 - Selfoss', '800 - Selfoss'),
    ('801 - Selfoss', '801 - Selfoss'),
    ('870 - Vík', '870 - Vík'),
    ('871 - Vík', '871 - Vík'),
    ('900 - Vestmannaeyjar', '900 - Vestmannaeyjar'),
    ('901 - Vestmannaeyjar', '901 - Vestmannaeyjar')
]

PROPERTY_TYPE_CHOICES = [
    ('Apartment', 'Apartment'),
    ('House', 'House'),
    ('Bungalow', 'Bungalow'),
    ('Villa', 'Villa'),
    ('Penthouse', 'Penthouse')
]

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    admin_approval = models.BooleanField(default=False)
    street =    models.CharField(max_length=100)
    house_number = models.IntegerField()
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    price = models.IntegerField()
    build_date = models.DateField()
    listing_date = models.DateTimeField(auto_now_add=True)
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




