# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Category, Product, Size, Color, Stock

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Stock)