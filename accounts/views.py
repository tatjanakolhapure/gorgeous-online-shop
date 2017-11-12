from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from accounts.forms import UserRegistrationForm, UserLoginForm

def login(request):
    if request.method == 'POST' and 'register' in request.POST:
        form_register = UserRegistrationForm(request.POST)

        if form_register.is_valid():
            form_register.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, "You have successfully registered")
                return redirect(reverse('account'))

            else:
                messages.error(request, "unable to log you in at this time!")

    else:
        form_register = UserRegistrationForm()

    if request.method == 'POST' and 'login' in request.POST:
        form_login = UserLoginForm(request.POST)
        if form_login.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                return redirect(reverse('account'))
            else:
                form_login.add_error(None, "Your email or password was not recognised")

    else:
        form_login = UserLoginForm()

    args = {'form_register': form_register, 'form_login': form_login}
    args.update(csrf(request))
    return render(request, 'login.html', args)


@login_required(login_url='/login/')
def account(request):
    return render(request, 'account.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('home'))