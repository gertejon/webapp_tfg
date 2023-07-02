from django.contrib import admin
from .models import Location, Stock


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

class LocationAdmin(admin.ModelAdmin):
    inlines = [StockInline]

admin.site.register(Location, LocationAdmin)