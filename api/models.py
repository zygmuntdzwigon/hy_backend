from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='company_logos')


class Event(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    banner = models.ImageField(upload_to='banners', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=128, null=False)
    event = models.ForeignKey(Event, related_name='products', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64)
    collect_from = models.DateTimeField()
    collect_to = models.DateTimeField()
    enabled = models.BooleanField()
    tag = models.CharField(max_length=128, null=False)

