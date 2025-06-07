from django.contrib import admin
from .models import CurrentCase, UserInventory

admin.site.register(CurrentCase)
admin.site.register(UserInventory)