# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

from home.views import get_index
from accounts.models import User
from products.models import Product

class HomePageTest(TestCase):

    fixtures = ['products', 'accounts']

    def setUp(self):
        super(HomePageTest, self).setUp()
        # get all products sold sorted by quantity
        sold_products = sorted([dict(quantity=sum([item.quantity for item in product.order_items.all()]),
                                     product=product, image=product.image_set.all()[0]) for product in
                                Product.objects.all()], key=lambda k: k['quantity'], reverse=True)
        # get 7 most sold products
        self.bestsellers = sold_products[:7]
        self.home_page = self.client.get('/')

    def test_home_page_resolves(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, get_index)

    def test_home_page_status_code_is_ok(self):
        self.assertEqual(self.home_page.status_code, 200)

    def test_home_page_uses_index_template(self):
        self.assertTemplateUsed(self.home_page, "home/index.html")

    def test_check_content_is_correct(self):
        home_page_template_output = render_to_response("home/index.html", {'bestsellers': self.bestsellers}).content
        self.assertEqual(self.home_page.content, home_page_template_output)

    def test_home_page_logged_in_content(self):
        user = User.objects.get(pk=16)
        self.client.login(username='karla.slinton@example.com', password='karlas')
        home_page = self.client.get('/')
        home_page_template_output = render_to_response("home/index.html", {'user': user, 'bestsellers': self.bestsellers}).content
        self.assertEquals(home_page.content, home_page_template_output)