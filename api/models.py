from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='company_logos')


class Address(models.Model):
    street = models.CharField(max_length=128)
    houseNumber = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    postalCode = models.CharField(max_length=32)


class Event(models.Model):
    name = models.CharField(max_length=128)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()
    banner = models.ImageField(upload_to='banners', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=128, null=False)
    event = models.ForeignKey(Event, related_name='products', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64)
    collectFrom = models.DateTimeField()
    collectTo = models.DateTimeField()
    enabled = models.BooleanField()
    tag = models.CharField(max_length=128, null=False)
