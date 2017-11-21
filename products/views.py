# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse

from .models import Category, Product, Size, Color

def products_list(request):

    selected_categories = None
    all_products = Product.objects.all()
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.GET.getlist('category'):
        selected_categories = Category.objects.filter(category__in=request.GET.getlist('category'))
        all_products = Product.objects.filter(category__in=selected_categories)

    # filter products which are in stock
    products_in_stock = list(set([product for product in all_products for stock in product.stock_set.all() if stock.amount > 0]))
    # create a list of products, each item is a dictionary with product object and image object
    products_list = [dict(product=product, image=product.image_set.all()[0]) for product in products_in_stock]
    # sort products by new in
    products_new_in = sorted(products_list, key=lambda k: k['product'].created, reverse=True)

    args = {
        'selected_categories': selected_categories,
        'categories': categories,
        'products': products_new_in,
        'sizes': sizes,
        'colors': colors,
    }

    # in case of ajax call update products html
    if request.is_ajax():
        html = render_to_string('filtered_products.html', {'products': products_new_in})
        return HttpResponse(html)

    return render(request, 'products_list.html', args)