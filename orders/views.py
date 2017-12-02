# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import OrderItem, Order
from accounts.models import Address
from products.models import Size
from cart.cart import Cart

@login_required(login_url='/login/')
def checkout(request):
    cart = Cart(request)
    user = request.user
    address = get_object_or_404(Address, user__exact=user)

    if request.method == 'POST':
        order = Order.objects.create(user=user, address=address)

        for item in cart:
            size = get_object_or_404(Size, size=item['size'])
            OrderItem.objects.create(order=order, product=item['product'], size=size, price=item['price'],
                                     quantity=item['quantity'])
        # clear the cart
        cart.clear()

    else:
        args = {'address': address, 'cart': cart}
        return render(request, 'checkout.html', args)
