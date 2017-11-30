from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product, Stock

# class created following instructions by Antonio Mele
# in the book Django By Example
class Cart(object):
    def __init__(self, request):
        # initialize the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart

    def add(self, product, size, quantity=1, update=False):
        # define dictionary for new product
        new_product = {'product_id': str(product.id), 'quantity': 1, 'price': str(product.price), 'size': size}
        size_object = product.size.filter(size=size)
        # get stock for the selected size
        stock = Stock.objects.get(product=product, size=size_object)

        # add product to the cart or update its quantity/size
        if self.cart:
            for item in self.cart:
                if item['product_id'] == str(product.id) and item['size'] == size:
                    if update:
                        # if product and size is in the list and it is update request
                        # update quantity
                        if (stock.amount - quantity) < 0:
                            return False
                        else:
                            item['quantity'] = quantity
                    else:
                        # if product and size is in the list and same product and size added
                        # increase quantity by one
                        if (stock.amount - item['quantity'] - quantity) < 0:
                            return False
                        else:
                            item['quantity'] += 1
                    self.save()
                    return True

            for item in self.cart:
                if item['product_id'] == str(product.id):
                    if update:
                        # if product is in the list and it is update request
                        # change size
                        item['size'] = size
                        # update quantity
                        if (stock.amount - quantity) < 0:
                            return False
                        else:
                            item['quantity'] = quantity
                    else:
                        # if product is in the list and same product added with different size
                        # add new size
                        self.cart.append(new_product)
                    self.save()
                    return True

            for item in self.cart:
                # if product is not in the cart add it
                if item['product_id'] != str(product.id):
                    self.cart.append(new_product)
                    self.save()
                    return True

        else:
            # if there are no items in the cart, add product
            self.cart.append(new_product)
            self.save()
            return True

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product_id, size):
        # remove the product from the cart
        for item in self.cart:
            if item['product_id'] == product_id and str(item['size']) == size:
                self.cart.remove(item)
        self.save()

    def __iter__(self):
        # iterate over the items in the cart and get the products from the database
        for item in self.cart:
            # get product
            product = Product.objects.get(pk=int(item['product_id']))
            item['product'] = product
            # get product image
            item['image'] = product.image_set.all()[0]
            # get all product sizes
            item['all_sizes'] = product.size.all()
            # filter stock where amount is more than 0 for the selected product
            stock = Stock.objects.filter(product=product, amount__gt=0)
            # get available sizes for the product, remove duplicates and sort by size field
            item['sizes_available'] = sorted(set([s.size for s in stock]), key=lambda k: k.size)
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # count all items in the cart
        return sum(item['quantity'] for item in self.cart)

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart)

    def get_delivery_price(self):
        if self.get_subtotal_price() > 75:
            return 0
        else:
            return 2.95

    def get_total_price(self):
        return round(self.get_subtotal_price() + Decimal(self.get_delivery_price()), 2)

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True