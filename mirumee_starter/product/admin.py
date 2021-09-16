from django.contrib import admin
from .models import Product
from .models import ProductVariant


admin.site.register(Product)
admin.site.register(ProductVariant)
