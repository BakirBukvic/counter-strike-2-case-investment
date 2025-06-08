from django.contrib import admin
from .models import CurrentCase, UserInventory, CasePriceHistory

@admin.register(CasePriceHistory)
class CasePriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('case', 'price', 'updated_at')

admin.site.register(CurrentCase)
admin.site.register(UserInventory)