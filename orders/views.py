# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import stripe

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib import messages

from .models import OrderItem, Order
from accounts.models import Address
from products.models import Size
from cart.cart import Cart
from .forms import PaymentForm

stripe.api_key = settings.STRIPE_SECRET

@login_required(login_url='/account/login/')
def checkout(request):
    cart = Cart(request)
    user = request.user
    address = get_object_or_404(Address, user__exact=user)
    form = PaymentForm()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        order = ''
        if form.is_valid():
            try:
                charge = stripe.Charge.create(
                    amount=int(cart.get_total_price()*100),
                    currency="GBP",
                    card=form.cleaned_data['stripe_id']
                )
                if charge.paid:
                    order = Order.objects.create(
                        user=user,
                        address='%s %s' % (address.house_number_name, address.street),
                        town=address.town,
                        postcode=address.postcode,
                        stripe_id=form.cleaned_data['stripe_id']
                    )
                    charge.description = 'Order %s for %s %s, %s' % (order.id, user.first_name, user.last_name, user.email)
                    charge.save()
                    for item in cart:
                        size = get_object_or_404(Size, size=item['size'])
                        OrderItem.objects.create(order=order, product=item['product'], size=size, price=item['price'],
                                                 quantity=item['quantity'])
                    # clear the cart
                    cart.clear()
                else:
                    messages.error(request, "We were unable to take a payment with that card")
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined")

        return redirect(reverse('order', kwargs={'order_id': order.id}))

    else:
        args = {'address': address, 'cart': cart, 'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
        return render(request, 'orders/checkout.html', args)


@login_required(login_url='/account/login/')
def order(request, order_id):
    return render(request, 'orders/order.html')