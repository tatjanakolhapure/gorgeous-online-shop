# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from tinymce import models as tinymce_models
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=40)

    class Meta:
        ordering = ['category']

    def __unicode__(self):
        return self.category

class Size(models.Model):
    size = models.CharField(max_length=20)

    class Meta:
        ordering = ['size']

    def __unicode__(self):
        return self.size

class Color(models.Model):
    color = models.CharField(max_length=20)

    class Meta:
        ordering = ['color']

    def __unicode__(self):
        return self.color

class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = tinymce_models.HTMLField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.ManyToManyField('Size')
    color = models.ManyToManyField('Color')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=True)
    image = models.ImageField(upload_to="images")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Stock(models.Model):
    amount = models.PositiveIntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)

    unique_together = ('product', 'size', 'color')