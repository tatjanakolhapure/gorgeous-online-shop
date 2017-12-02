# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Category, Product, Size, Color, Image, Stock

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
admin.site.register(Category, CategoryAdmin)

class ImageInline(admin.TabularInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'created']
    list_filter = ['category__category', 'size__size', 'color__color', 'created']
    list_editable = ['price']
    inlines = [ImageInline]

admin.site.register(Product, ProductAdmin)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']

admin.site.register(Size, SizeAdmin)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']

admin.site.register(Color, ColorAdmin)

class StockAdmin(admin.ModelAdmin):
    list_display = ['amount', 'product', 'size', 'color']
    list_filter = ['product__name', 'size__size', 'color__color']
admin.site.register(Stock, StockAdmin)