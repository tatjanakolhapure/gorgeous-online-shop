# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import resolve

from .views import *
from .forms import CartForm
from products.models import Product, Stock

class CartPageTest(TestCase):

    def setUp(self):
        super(CartPageTest, self).setUp()
        self.cart_page = self.client.get('/cart/')

    def test_cart_page_resolves(self):
        cart_page = resolve('/cart/')
        self.assertEqual(cart_page.func, cart_detail)

    def test_cart_page_status_code_is_ok(self):
        self.assertEqual(self.cart_page.status_code, 200)

    def test_cart_page_uses_correct_template(self):
        self.assertTemplateUsed(self.cart_page, "cart/cart.html")


class CartFormTest(TestCase):

    def test_cart_form_quantity_choices(self):
        choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]
        form = CartForm()
        self.assertEqual(choices, form.fields['quantity'].choices)

    def test_cart_form_without_update(self):
        form = CartForm({
            'quantity': '1',
        })
        self.assertTrue(form.is_valid())

    def test_cart_form_with_update(self):
        form = CartForm({
            'quantity': '2',
            'update': True
        })
        self.assertTrue(form.is_valid())


class CartUpdateTest(TestCase):

    fixtures = ['products', 'accounts']

    def setUp(self):
        super(CartUpdateTest, self).setUp()
        self.product = Product.objects.get(pk=10)
        self.client.login(username='karla.slinton@example.com', password='karlas')
        cart_update_page = self.client.post('/cart/add/10', {'size': 'UK 8', 'quantity': '1', 'update': 'False'})
        request = cart_update_page.wsgi_request
        self.cart = Cart(request)
        self.size = request.POST['size']
        form = CartForm(request.POST)
        form.is_valid()
        # add product to the cart
        self.updated_cart = self.cart.add(product=self.product, size=self.size,
                                quantity=form.cleaned_data['quantity'],
                                update=form.cleaned_data['update'])

    def test_cart_add_item(self):
        # confirm that product was added
        self.assertTrue(self.updated_cart)
        # get stock for the product
        stock = Stock.objects.filter(product=self.product, amount__gt=0)
        # check all values for item in the cart
        for item in self.cart:
            self.assertEqual(item['product'], self.product)
            self.assertEqual(item['total_price'], item['price'] * item['quantity'])
            self.assertEqual(item['product_id'], str(self.product.id))
            self.assertEqual(item['sizes_available'], sorted(set([s.size for s in stock]), key=lambda k: k.size))
            self.assertEqual(item['quantity'], 1)
            self.assertEqual(item['image'], self.product.image_set.all()[0])
            self.assertEqual(item['size'], 'UK 8')
            # check that all product sizes are in the cart
            for size in self.product.size.all():
                for item in self.cart:
                    if size in item['all_sizes']:
                        self.assertTrue(size in item['all_sizes'])

    def test_cart_update_product_size(self):
        # update product's size
        cart_update_page = self.client.post('/cart/add/10', {'size': 'UK 6', 'quantity': '1', 'update': 'True'})
        request = cart_update_page.wsgi_request
        size = request.POST['size']
        form = CartForm(request.POST)
        form.is_valid()
        updated_cart = self.cart.add(product=self.product, size=size, quantity=form.cleaned_data['quantity'],
                                update=form.cleaned_data['update'])
        # confirm that cart was updated
        self.assertTrue(updated_cart)
        # check product size
        for item in self.cart:
            self.assertEqual(item['size'], 'UK 6')
            self.assertEqual(item['quantity'], 1)

    def test_cart_update_product_quantity(self):
        # update product's quantity
        cart_update_page = self.client.post('/cart/add/10', {'size': 'UK 8', 'quantity': '3', 'update': 'True'})
        request = cart_update_page.wsgi_request
        size = request.POST['size']
        form = CartForm(request.POST)
        form.is_valid()
        updated_cart = self.cart.add(product=self.product, size=size, quantity=form.cleaned_data['quantity'],
                                update=form.cleaned_data['update'])
        # confirm that cart was updated
        self.assertTrue(updated_cart)
        # check product size
        for item in self.cart:
            self.assertEqual(item['size'], 'UK 8')
            self.assertEqual(item['quantity'], 3)

    def test_cart_update_product_size_and_quantity(self):
        # update product's size and quantity
        cart_update_page = self.client.post('/cart/add/10', {'size': 'UK 6', 'quantity': '2', 'update': 'True'})
        request = cart_update_page.wsgi_request
        size = request.POST['size']
        form = CartForm(request.POST)
        form.is_valid()
        updated_cart = self.cart.add(product=self.product, size=size, quantity=form.cleaned_data['quantity'],
                                update=form.cleaned_data['update'])
        # confirm that cart was updated
        self.assertTrue(updated_cart)
        # check product size and quantity
        for item in self.cart:
            self.assertEqual(item['size'], 'UK 6')
            self.assertEqual(item['quantity'], 2)

    def test_cart_add_different_product(self):
        # update product's size and quantity
        product = Product.objects.get(pk=11)
        cart_update_page = self.client.post('/cart/add/11', {'size': 'UK 6', 'quantity': '1', 'update': 'False'})
        request = cart_update_page.wsgi_request
        size = request.POST['size']
        form = CartForm(request.POST)
        form.is_valid()
        updated_cart = self.cart.add(product=product, size=size, quantity=form.cleaned_data['quantity'],
                                     update=form.cleaned_data['update'])
        # confirm that cart was updated
        self.assertTrue(updated_cart)
        # check if there are two products in the cart
        product_one = {}
        product_two = {}
        for item in self.cart:
            if item['product'] == self.product:
                product_one = item
            else:
                product_two = item
        # check that cart has both products and correct size and quantity for the new product
        self.assertEqual(product_one['product'], self.product)
        self.assertEqual(product_two['product'], product)
        self.assertEqual(product_two['quantity'], 1)
        self.assertEqual(product_two['size'], 'UK 6')

    def test_cart_update_product_quantity_not_in_stock(self):
        # update product's quantity
        cart_update_page = self.client.post('/cart/add/10', {'size': 'UK 8', 'quantity': '8', 'update': 'True'})
        request = cart_update_page.wsgi_request
        size = request.POST['size']
        form = CartForm(request.POST)
        form.is_valid()
        updated_cart = self.cart.add(product=self.product, size=size, quantity=form.cleaned_data['quantity'],
                                     update=form.cleaned_data['update'])
        # confirm that cart was not updated
        self.assertFalse(updated_cart)
        # check if product has the same size and quantity in the cart
        for item in self.cart:
            self.assertEqual(item['size'], 'UK 8')
            self.assertEqual(item['quantity'], 1)

