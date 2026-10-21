from django.db import models

class Asset(models.Model):
    ticker = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200, blank=True)
    asset_type = models.CharField(max_length=50, blank=True)  # stock, etf, crypto
    sector = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker


class PriceHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    timeframe = models.CharField(max_length=10)  # 1d, 4h, 1h
    open = models.DecimalField(max_digits=20, decimal_places=6)
    high = models.DecimalField(max_digits=20, decimal_places=6)
    low = models.DecimalField(max_digits=20, decimal_places=6)
    close = models.DecimalField(max_digits=20, decimal_places=6)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('asset', 'datetime', 'timeframe')
        verbose_name_plural = 'Price History'

    def __str__(self):
        return f"{self.asset.ticker} {self.timeframe} {self.datetime}"


class Fundamentals(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()

    # Earnings
    days_to_earnings = models.IntegerField(null=True, blank=True)

    # Valoracion
    pe_trailing = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    pe_forward = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    price_to_book = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    ev_to_ebitda = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    price_to_sales = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    # Rentabilidad
    profit_margin = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    operating_margin = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    roe = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    roa = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    # Crecimiento
    revenue_growth = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    earnings_growth = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    # Salud financiera
    debt_to_equity = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    current_ratio = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    total_cash = models.BigIntegerField(null=True, blank=True)
    total_debt = models.BigIntegerField(null=True, blank=True)

    # Tamanio
    market_cap = models.BigIntegerField(null=True, blank=True)
    enterprise_value = models.BigIntegerField(null=True, blank=True)
    total_revenue = models.BigIntegerField(null=True, blank=True)
    ebitda = models.BigIntegerField(null=True, blank=True)

    # Dividendos
    dividend_yield = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    dividend_rate = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    payout_ratio = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('asset', 'date')
        verbose_name_plural = 'Fundamentals'

    def __str__(self):
        return f"{self.asset.ticker} {self.date}"
