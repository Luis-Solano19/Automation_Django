from django.contrib import admin
from.models import Stock, StockData

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'symbol', 'exchange')
    
admin.site.register(Stock, StockAdmin)
admin.site.register(StockData)