from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from products.models import Product
from .cart import Cart
from .forms import CartForm

# views created following instructions by Antonio Mele
# in the book Django By Example
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    # get product object by id
    product = get_object_or_404(Product, id=product_id)
    # get selected size from request data
    size = request.POST['size']
    form = CartForm(request.POST)

    if form.is_valid():
        # add product to the cart
        # or update it's quantity/ size
        updated_cart = cart.add(product=product, size=size, quantity=form.cleaned_data['quantity'],
                                update=form.cleaned_data['update'])
        if updated_cart:
            # if cart updated return success status
            return HttpResponse(status=200)
        else:
            # if cart not updated return error message
            return HttpResponse(status=400)

def cart_remove(request, product_id, size):
    cart = Cart(request)
    cart.remove(product_id, size)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        # create form for each item in the cart
        # to allow updating its quantity and size
        item['update_quantity_form'] = CartForm(initial={'quantity': item['quantity'],'update': True})
    args = {'cart': cart}
    return render(request, 'cart.html', args)