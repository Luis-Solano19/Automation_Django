from django.db import models

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50) # Unique stock symbol
    sector = models.CharField(max_length=100, null=True, blank=True) # Sector e.g Technology, Financial, etc.
    exchange = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name


class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    current_price = models.CharField(max_length=25, null=True, blank=True)
    price_changed = models.CharField(max_length=25, null=True, blank=True) # previous closed - current_price
    percentage_changed = models.CharField(max_length=25, null=True, blank=True) # (Precio Actual - Cierre anterior / Cierrer anterior) *100
    previous_close = models.CharField(max_length=25, null=True, blank=True)
    week_52_high = models.CharField(max_length=25, null=True, blank=True) # intervalo anual
    week_52_low = models.CharField(max_length=25, null=True, blank=True) # intervalo anual
    daily_high = models.CharField(max_length=25, null=True, blank=True) # intervalo diario
    daily_low = models.CharField(max_length=25, null=True, blank=True) # intervalo diario
    market_cap = models.CharField(max_length=25, null=True, blank=True) # cap. bursatil
    pe_ratio = models.CharField(max_length=25, null=True, blank=True) # RELACIÓN PRECIO-BENEFICIO
    
    
    def __str__(self):
        return f"{self.stock} - {self.current_price}"
    
    class Meta:
        verbose_name_plural = "StockData"
    