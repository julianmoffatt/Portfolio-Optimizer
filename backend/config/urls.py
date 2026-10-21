from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.market_data.urls')),
    path('api/', include('apps.portfolio.urls')),
]
