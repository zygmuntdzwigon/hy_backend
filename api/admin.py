from django.contrib import admin
from .models import Event, UserProfile, Product, Address

# Register your models here.
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Address)
