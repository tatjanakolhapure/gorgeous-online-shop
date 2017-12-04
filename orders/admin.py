# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'town', 'postcode', 'status', 'stripe_id',
                    'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)