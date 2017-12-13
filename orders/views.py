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
from products.models import Size, Stock
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
                # create stripe charge object
                charge = stripe.Charge.create(
                    # amount in units
                    amount=int(float(cart.get_total_price())*100),
                    currency="GBP",
                    card=form.cleaned_data['stripe_id']
                )
                if charge.paid:
                    # create order if charge was created successfully and paid
                    order = Order.objects.create(
                        user=user,
                        # save address in one string
                        address='%s %s' % (address.house_number_name, address.street),
                        town=address.town,
                        postcode=address.postcode,
                        stripe_id=form.cleaned_data['stripe_id']
                    )
                    # add description to charge giving order details
                    charge.description = 'Order %s for %s %s, %s' % (order.id, user.first_name, user.last_name, user.email)
                    charge.save()
                    for item in cart:
                        size = get_object_or_404(Size, size=item['size'])
                        product = item['product']
                        stock = get_object_or_404(Stock, product=product, size=size)
                        # create order item for each product in the cart
                        OrderItem.objects.create(order=order, product=product, size=size, price=item['price'],
                                                 quantity=item['quantity'])
                        # update stock for each product
                        stock.amount -= item['quantity']
                        stock.save()
                    # clear the cart
                    cart.clear()
                else:
                    messages.error(request, "We were unable to take a payment with that card")
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined")
        # redirect to order page
        return redirect(reverse('order', kwargs={'order_id': order.id}))

    else:
        args = {'address': address, 'cart': cart, 'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
        return render(request, 'orders/checkout.html', args)


@login_required(login_url='/account/login/')
def order(request, order_id):
    order=get_object_or_404(Order, id=order_id)
    order_data = dict(order=order, total=order.get_total_cost(), subtotal=order.get_subtotal_cost(),
             delivery=order.get_delivery_cost(), date=order.created.strftime('%d %b %Y'))
    order_items = [dict(item=item, image=item.product.image_set.all()[0]) for item in order.items.all()]
    args={'order': order_data, 'order_items': order_items}
    return render(request, 'orders/order.html', args)


@login_required(login_url='/account/login/')
def orders_list(request):
    user = request.user
    orders = Order.objects.filter(user__exact=user)
    orders_data = [
        dict(order=order, total=order.get_total_cost(),
        items=sum([item.quantity for item in order.items.all()]), date=order.created.strftime('%d %b %y'))
        for order in orders
    ]
    args= {'orders': orders_data}
    return render(request, 'orders/orders_list.html', args)