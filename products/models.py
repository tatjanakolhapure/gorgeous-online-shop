# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=40)

class Size(models.Model):
    name = models.CharField(max_length=20)

class Color(models.Model):
    name = models.CharField(max_length=20)

class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.ManyToManyField('Size')
    color = models.ManyToManyField('Color')
    created = models.DateTimeField(default=timezone.now)

class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")

class Stock(models.Model):
    amount = models.PositiveIntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)