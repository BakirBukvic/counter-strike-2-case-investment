from django.db import models
from django.utils import timezone
# Create your models here.


class CurrentCase(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hash_search = models.CharField(max_length=255, unique=True)
    last_price_update = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        price_changed = False
        if self.pk is not None:
            orig = CurrentCase.objects.get(pk=self.pk)
            if orig.price != self.price:
                self.last_price_update = timezone.now()
                price_changed = True
        else:
            self.last_price_update = timezone.now()
            price_changed = True
        super().save(*args, **kwargs)
        if price_changed and self.price is not None:
            from .models import CasePriceHistory
            CasePriceHistory.objects.create(case=self, price=self.price)
    def __str__(self):
        return self.name


class CasePriceHistory(models.Model):
    case = models.ForeignKey(CurrentCase, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserInventory(models.Model):
    case_bought = models.ForeignKey(CurrentCase, on_delete=models.CASCADE)
    ammount = models.PositiveIntegerField(default=0)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    buy_date = models.DateTimeField()