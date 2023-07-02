from django.contrib import admin
from .models import Product
from categories.models import Category
from product_types.models import Product_Type
from brands.models import Brand


class ProductAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "accessories":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(is_accessory=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Product, ProductAdmin)