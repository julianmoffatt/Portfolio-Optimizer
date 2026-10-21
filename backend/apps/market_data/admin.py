from django.contrib import admin
from .models import Asset, PriceHistory, Fundamentals

admin.site.register(Asset)
admin.site.register(PriceHistory)
admin.site.register(Fundamentals)
