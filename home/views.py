# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils import timezone
from django.shortcuts import render

from products.models import Product

def get_index(request):
    # code for filtering popular products within last week or month

    # get the datetime for the beginning of the current month
    # now = timezone.now()
    # today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # month_start = today.replace(day=1)

    # datetime for the beginning of the week
    #week_start = today - datetime.timedelta(days=datetime.datetime.today().weekday())

    # get all products sold
    sold_products = sorted([
        dict(quantity=sum([item.quantity for item in product.order_items.all()]),
        product=product, image=product.image_set.all()[0]) for product in Product.objects.all()],
        key=lambda k: k['quantity'], reverse=True)

    # get 7 most sold products
    bestsellers = sold_products[:7]

    args = {'bestsellers': bestsellers}

    return render(request, 'home/index.html', args)