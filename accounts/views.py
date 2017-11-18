import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError

from django.conf import settings
from accounts.models import Address, User
from accounts.forms import UserRegistrationForm, UserLoginForm, AddressFrom, UserDetailsFrom

def login(request):
    if request.method == 'POST' and 'register' in request.POST:
        form_register = UserRegistrationForm(request.POST)
        form_address = AddressFrom(request.POST)

        try:
            if all([form_register.is_valid(), form_address.is_valid()]):
                user = form_register.save()
                address = form_address.save(commit=False)
                address.user = user
                address.save()

                user = auth.authenticate(email=request.POST.get('email'),
                                         password=request.POST.get('password1'))
                if user:
                    auth.login(request, user)
                    return JsonResponse({"status":"200"})
                else:
                    return JsonResponse({"message": "Your email or password was not recognised"}, status=404)

        except IntegrityError:
            return JsonResponse({"message": "User with this email already exists"}, status=404)
        else:
            return JsonResponse({"message": "Passwords do not match"}, status=404)

    else:
        form_register = UserRegistrationForm()
        form_address = AddressFrom()

    if request.method == 'POST' and 'login' in request.POST:

        form_login = UserLoginForm(request.POST)
        if form_login.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))
            if user is not None:
                auth.login(request, user)
                return JsonResponse({"status": "200"})
            else:
                return JsonResponse({"message": "Your email or password was not recognised"}, status=404)

    else:
        form_login = UserLoginForm()

    args = {'form_register': form_register, 'form_address': form_address, 'form_login': form_login}
    args.update(csrf(request))
    return render(request, 'login.html', args)

@login_required(login_url='/login/')
def account(request):
    user = request.user
    try:
        address = get_object_or_404(Address, user=user)
    except Exception as e:
        address = None
    return render(request, 'account.html', {'address': address})


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


@login_required
def edit_address(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    address = get_object_or_404(Address, user=user)

    if request.method == "POST":
        form = AddressFrom(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(reverse('account'))
    else:
        form = AddressFrom(instance=address)

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'account_address_form.html', args)

@login_required
def edit_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = UserDetailsFrom(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('account'))
    else:
        form = UserDetailsFrom(instance=user)

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'account_details_form.html', args)