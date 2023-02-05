from django.contrib import admin

from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    fields = ("category", "author", "name", "description", "price", "image")


admin.site.register(Category)
admin.site.register(Product)  # , ProductAdmin)
