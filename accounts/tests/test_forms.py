# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from accounts.views import *
from accounts.forms import UserLoginForm, UserRegistrationForm, AddressForm, UserDetailsForm

class LoginFormTest(TestCase):

    fixtures = ['accounts']

    def test_login_form(self):
        form = UserLoginForm({
            'login_email': 'karla.slinton@example.com',
            'password': 'karlas',
        })
        self.assertTrue(form.is_valid())

    def test_login_form_fails_with_incorrect_email(self):
        form = UserLoginForm({
            'login_email': 'karla.slinton',
            'password': 'karlas',
        })
        self.assertFalse(form.is_valid())

    def test_login_form_fails_without_password(self):
        form = UserLoginForm({
            'login_email': 'karla.slinton@example.com',
        })
        self.assertFalse(form.is_valid())

    def test_login_existing_user(self):
        login = self.client.login(username='karla.slinton@example.com', password='karlas')
        self.assertTrue(login)

    def test_login_fails_with_non_existing_user(self):
        login = self.client.login(username='karla@example.com', password='karlas')
        self.assertFalse(login)


class RegistrationFormTest(TestCase):

    fixtures = ['accounts']

    def test_registration_form_and_login(self):
        form = UserRegistrationForm({
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test.user@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        # check if form is valid
        self.assertTrue(form.is_valid())
        # save user and try to login
        form.save()
        login = self.client.login(username='test.user@example.com', password='testpassword')
        # check if user is logged in
        self.assertTrue(login)

    def test_registration_form_fails_with_passwords_that_dont_match(self):
        form = UserRegistrationForm({
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test.user@example.com',
            'password1': 'testpassword',
            'password2': 'testpasswor2',
        })
        self.assertFalse(form.is_valid())

    def test_registration_form_fails_without_first_name(self):
        form = UserRegistrationForm({
            'last_name': 'user',
            'email': 'test.user@example.com',
            'password1': 'testpassword',
            'password2': 'testpasswor',
        })
        self.assertFalse(form.is_valid())

    def test_registration_fails_with_existing_email(self):
        form = UserRegistrationForm({
            'first_name': 'test',
            'last_name': 'user',
            'email': 'karla.slinton@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        form.is_valid()
        with self.assertRaises(IntegrityError): form.save()


class AddressFormTest(TestCase):

    fixtures = ['accounts']

    def test_address_form(self):
        form = AddressForm({
            'house_number_name': '8 house',
            'street': '11 test street',
            'town': 'test town',
            'postcode': 'sss',
        })
        self.assertTrue(form.is_valid())
        # get user
        user = User.objects.get(pk=16)
        # assign user to address
        address = form.save(commit=False)
        address.user = user
        # save address
        address.save()
        # check if saved address is user's address now
        self.assertTrue(address, user.address_set.all())

    def test_address_form_fails_without_some_field(self):
        form = AddressForm({
            'house_number_name': '8 house',
            'street': '11 test street',
            'town': 'test town',
        })
        self.assertFalse(form.is_valid())


class UserDetailsFormTest(TestCase):

    fixtures = ['accounts']

    def setUp(self):
        super(UserDetailsFormTest, self).setUp()
        self.user = User.objects.get(pk=16)

    def test_changing_user_first_name(self):
        form =  UserDetailsForm({
            'first_name': 'Elizabeth',
            'last_name': self.user.last_name,
            'email': self.user.email,
        }, instance=self.user)

        self.assertTrue(form.is_valid())
        # save details
        form.save()
        # check if new name is user's name now
        self.assertTrue('Elizabeth', self.user.first_name)

    def test_user_details_form_fails_without_last_name(self):
        form =  UserDetailsForm({
            'first_name': self.user.first_name,
            'email': self.user.email,
        }, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_user_details_form_fails_with_incorrect_email(self):
        form =  UserDetailsForm({
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'test_email.com',
        }, instance=self.user)
        self.assertFalse(form.is_valid())