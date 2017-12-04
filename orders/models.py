# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.conf import settings

from products.models import Product, Size
from accounts.models import Address

class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # save address as a string instead as a foreign key to address model
    # so the address cannot be changed
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=40)
    postcode = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Processing', max_length=20)
    stripe_id = models.CharField(max_length=40, default='')

    class Meta:
        ordering = ('-created',)

    def get_subtotal_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_delivery_cost(self):
        if self.get_subtotal_cost() > 75:
            return '{0:.2f}'.format(0)
        else:
            return '{0:.2f}'.format(2.95)

    def get_total_cost(self):
        return '{0:.2f}'.format(round(self.get_subtotal_cost() + Decimal(self.get_delivery_cost()), 2))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    size = models.ForeignKey(Size)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity