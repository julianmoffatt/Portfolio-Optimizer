from django.db import models
from apps.market_data.models import Asset


class Portfolio(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # peso en %, ej: 25.50

    class Meta:
        unique_together = ('portfolio', 'asset')

    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.ticker} ({self.weight}%)"
