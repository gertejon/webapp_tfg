from django.contrib import admin
from .models import Order, OrderProduct


class ProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)