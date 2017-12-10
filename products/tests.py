# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render_to_response

from products.views import *
from products.models import Product, Category, Size, Color

class ProductsListPageTest(TestCase):

    fixtures = ['products']

    def setUp(self):
        super(ProductsListPageTest, self).setUp()
        self.products_list_page = self.client.get('/products/')
        self.categories = Category.objects.all()
        self.sizes = Size.objects.all()
        self.colors = Color.objects.all()

    def test_products_list_page_resolves(self):
        products_list_page = resolve('/products/')
        self.assertEqual(products_list_page.func, products_list)

    def test_products_list_page_status_code_is_ok(self):
        self.assertEqual(self.products_list_page.status_code, 200)

    def test_products_list_page_uses_correct_template(self):
        self.assertTemplateUsed(self.products_list_page, "products/products_list.html")

    def test_products_list_page_content_all_products(self):
        # filter all products which are in stock
        products_in_stock = list(set([product for product in Product.objects.all() for stock in product.stock_set.all() if stock.amount > 0]))
        # create a list of products, each item is a dictionary with product object and image object
        products_list = [dict(product=product, image=product.image_set.all()[0]) for product in products_in_stock]
        # sort products by new in by default
        products_sorted = sorted(products_list, key=lambda k: k['product'].created, reverse=True)
        paginator = Paginator(products_sorted, 8)  # Show certain amount of products per page
        products = paginator.page(1)
        args = {
            'selected_categories': None,
            'products': products,
            'categories': self.categories,
            'category': None,
            'sizes': self.sizes,
            'colors': self.colors,
            'current_page': 1,
            'pages_range': paginator.page_range
        }
        products_list_page_template_output = render_to_response("products/products_list.html", args).content
        self.assertEquals(self.products_list_page.content, products_list_page_template_output)

    def test_products_list_page_content_all_products_sorted_low_to_high(self):
        products_list_page = self.client.get('/products/?sort=low-to-high')
        # filter all products which are in stock
        products_in_stock = list(set([product for product in Product.objects.all() for stock in product.stock_set.all() if stock.amount > 0]))
        # create a list of products, each item is a dictionary with product object and image object
        products_list = [dict(product=product, image=product.image_set.all()[0]) for product in products_in_stock]
        # sort products by low to high
        products_sorted = sorted(products_list, key=lambda k: k['product'].price)
        paginator = Paginator(products_sorted, 8)  # Show certain amount of products per page
        products = paginator.page(1)
        args = {
            'selected_categories': None,
            'products': products,
            'categories': self.categories,
            'category': None,
            'sizes': self.sizes,
            'colors': self.colors,
            'current_page': 1,
            'pages_range': paginator.page_range
        }
        products_list_page_template_output = render_to_response("products/products_list.html", args).content
        self.assertEquals(products_list_page.content, products_list_page_template_output)

    def test_products_list_page_content_dresses(self):
        products_list_page = self.client.get('/products/dresses/')
        category = get_object_or_404(Category, category='dresses')
        # filter products which are in stock
        products_in_stock = list(set([product for product in Product.objects.filter(category=category) for stock in product.stock_set.all() if stock.amount > 0]))
        # create a list of products, each item is a dictionary with product object and image object
        products_list = [dict(product=product, image=product.image_set.all()[0]) for product in products_in_stock]
        # sort products by new in by default
        products_sorted = sorted(products_list, key=lambda k: k['product'].created, reverse=True)
        paginator = Paginator(products_sorted, 8)  # Show certain amount of products per page
        products = paginator.page(1)
        args = {
            'selected_categories': None,
            'products': products,
            'categories': self.categories,
            'category': category,
            'sizes': self.sizes,
            'colors': self.colors,
            'current_page': 1,
            'pages_range': paginator.page_range
        }
        products_list_page_template_output = render_to_response("products/products_list.html", args).content
        self.assertEquals(products_list_page.content, products_list_page_template_output)

    def test_products_list_page_content_dresses_tops_black_size_eight_ten(self):
        products_list_page = self.client.get('/products/?category=dresses,tops&color=black&size=UK 8, UK 10')
        request = products_list_page.wsgi_request

        selected_categories = Category.objects.filter(category__in=request.GET.getlist('category'))
        selected_color = Color.objects.get(color__in=request.GET.getlist('color'))
        selected_sizes_objects = Size.objects.filter(size__in=request.GET.getlist('size'))
        selected_sizes = [size.size for size in selected_sizes_objects]

        selected_products = [product for product in Product.objects.all()
                                         if product.category in selected_categories
                                         if product.color.filter(color=selected_color.color)
                                         if product.size.filter(size__in=selected_sizes)]

        # filter products which are in stock
        products_in_stock = list(set([product for product in selected_products for stock in product.stock_set.all() if stock.amount > 0]))
        # create a list of products, each item is a dictionary with product object and image object
        products_list = [dict(product=product, image=product.image_set.all()[0]) for product in products_in_stock]
        # sort products by new in by default
        products_sorted = sorted(products_list, key=lambda k: k['product'].created, reverse=True)
        paginator = Paginator(products_sorted, 8)  # Show certain amount of products per page
        products = paginator.page(1)
        args = {
            'selected_categories': selected_categories,
            'products': products,
            'categories': self.categories,
            'category': None,
            'sizes': self.sizes,
            'colors': self.colors,
            'current_page': 1,
            'pages_range': paginator.page_range
        }
        products_list_page_template_output = render_to_response("products/products_list.html", args).content
        self.assertEquals(products_list_page.content, products_list_page_template_output)