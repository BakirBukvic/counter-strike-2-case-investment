from django.db import models

# Create your models here.


class CurrentCase(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hash_search = models.CharField(max_length=255, unique=True)


class UserInventory(models.Model):
    case_bought = models.ForeignKey(CurrentCase, on_delete=models.CASCADE)
    ammount = models.PositiveIntegerField(default=0)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    buy_date = models.DateTimeField(auto_now_add=True)