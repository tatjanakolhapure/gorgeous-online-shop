# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

from accounts.models import User
from .views import *

class OrderListPageTest(TestCase):

    fixtures = ['accounts', 'products', 'orders']

    def setUp(self):
        super(OrderListPageTest, self).setUp()
        self.client.login(username='silvia.consila@example.com', password='italy123')
        self.orders_list_page = self.client.get('/orders/')

    def test_orders_list_page_resolves(self):
        orders_list_page = resolve('/orders/')
        self.assertEqual(orders_list_page.func, orders_list)

    def test_orders_list_page_status_code_is_ok(self):
        self.assertEqual(self.orders_list_page.status_code, 200)

    def test_orders_list_page_uses_correct_template(self):
        self.assertTemplateUsed(self.orders_list_page, "orders/orders_list.html")

    def test_orders_list_page_content(self):
        user = User.objects.get(pk=31)
        orders = Order.objects.filter(user__exact=user)
        orders_data = [
            dict(order=order, total=order.get_total_cost(),
            items=sum([item.quantity for item in order.items.all()]), date=order.created.strftime('%d %b %y'))
            for order in orders
            ]

        orders_list_page_template_output = render_to_response("orders/orders_list.html",
                                                          {'orders': orders_data, 'user' : user}).content
        self.assertEquals(self.orders_list_page.content, orders_list_page_template_output)

class OrderPageTest(TestCase):

    fixtures = ['accounts', 'products', 'orders']

    def setUp(self):
        super(OrderPageTest, self).setUp()
        self.order = get_object_or_404(Order, id=7)
        self.client.login(username='silvia.consila@example.com', password='italy123')
        self.order_page = self.client.get('/orders/%s/' % self.order.id)

    def test_order_page_resolves(self):
        order_page = resolve('/orders/%s/' % self.order.id)
        self.assertEqual(order_page.func, order)

    def test_order_page_status_code_is_ok(self):
        self.assertEqual(self.order_page.status_code, 200)

    def test_order_page_uses_correct_template(self):
        self.assertTemplateUsed(self.order_page, "orders/order.html")

    def test_order_page_content(self):
        user = User.objects.get(pk=31)
        order_data = dict(order=self.order, total=self.order.get_total_cost(), subtotal=self.order.get_subtotal_cost(),
                          delivery=self.order.get_delivery_cost(), date=self.order.created.strftime('%d %b %Y'))
        order_items = [dict(item=item, image=item.product.image_set.all()[0]) for item in self.order.items.all()]
        order_page_template_output = render_to_response("orders/order.html",
                                        {'order': order_data, 'order_items': order_items, 'user': user}).content
        self.assertEquals(self.order_page.content, order_page_template_output)

    def test_order_prices(self):
        self.assertEqual(self.order.get_total_cost(), '149.00')
        self.assertEqual(self.order.get_delivery_cost(), '0.00')
        self.assertEqual(self.order.get_subtotal_cost(), '149.00')

class CheckoutPageTest(TestCase):

    fixtures = ['accounts']

    def setUp(self):
        super(CheckoutPageTest, self).setUp()
        self.client.login(username='karla.slinton@example.com', password='karlas')
        self.checkout_page = self.client.get('/orders/checkout/')

    def test_checkout_page_resolves(self):
        checkout_page = resolve('/orders/checkout/')
        self.assertEqual(checkout_page.func, checkout)

    def test_checkout_page_status_code_is_ok(self):
        self.assertEqual(self.checkout_page.status_code, 200)

    def test_checkout_page_uses_correct_template(self):
        self.assertTemplateUsed(self.checkout_page, "orders/checkout.html")
