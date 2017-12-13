# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.conf import settings

from accounts.models import User
from .views import *
from .forms import PaymentForm

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

class PaymentFormTest(TestCase):

    def setUp(self):
        self.expiry_year = str(datetime.datetime.today().year+1)[-2:]

    def test_payment_form_month_choices(self):
        choices = [
            ('', 'MM'),
            ('1', '01'), ('2', '02'), ('3', '03'),
            ('4', '04'), ('5', '05'), ('6', '06'),
            ('7', '07'), ('8', '08'), ('9', '09'),
            ('10', '10'), ('11', '11'), ('12', '12'),
        ]
        form = PaymentForm()
        self.assertEqual(choices, form.fields['expiry_month'].choices)

    def test_payment_form_year_choices(self):
        choices = [
            ('', 'YY'),
            (17, 17), (18, 18), (19, 19),
            (20, 20), (21, 21), (22, 22),
            (23, 23), (24, 24), (25, 25),
        ]
        form = PaymentForm()
        self.assertEqual(choices, form.fields['expiry_year'].choices)

    def test_payment_form(self):
        form = PaymentForm({
            'address_line1': '10 House Name',
            'address_line2': '21 Street Name',
            'address_city': 'Test City',
            'address_zip': 'SSS',
            'name': 'Jason Smith',
            'card_number': '4242424242424242',
            'expiry_month': '2',
            'expiry_year': self.expiry_year,
            'cvv': '333',
            'stripe_id': 'teststripe478',
        })
        self.assertTrue(form.is_valid())

    def test_payment_form_fails_without_expiry_month(self):
        form = PaymentForm({
            'address_line1': '10 House Name',
            'address_line2': '21 Street Name',
            'address_city': 'Test City',
            'address_zip': 'SSS',
            'name': 'Jason Smith',
            'card_number': '4242424242424242',
            'expiry_year': self.expiry_year,
            'cvv': '333',
            'stripe_id': 'teststripe478',
        })
        self.assertFalse(form.is_valid())

    def test_payment_form_without_stripe_id(self):
        form = PaymentForm({
            'address_line1': '10 House Name',
            'address_line2': '21 Street Name',
            'address_city': 'Test City',
            'address_zip': 'SSS',
            'name': 'Jason Smith',
            'card_number': '4242424242424242',
            'expiry_month': '2',
            'expiry_year': self.expiry_year,
            'cvv': '333',
        })
        self.assertTrue(form.is_valid())

class StripeChargeTest(TestCase):

    stripe.api_key = settings.STRIPE_SECRET

    def setUp(self):
        expiry_year = str(datetime.datetime.today().year + 1)[-2:]
        # get token for creating a charge
        self.token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '6',
                'exp_year': expiry_year,
                'cvc': '123',
            })

    def test_stripe_create_and_update_charge(self):
        charge = stripe.Charge.create(
            amount=7500,
            currency="GBP",
            card=self.token
        )
        # check if charge has been paid
        self.assertEqual(charge.paid, True)
        description = 'Order 1 for Jason Smith, jason.smith@example.com'
        charge.description = description
        charge.save()
        #check if description has been updated
        self.assertEqual(charge.description, description)