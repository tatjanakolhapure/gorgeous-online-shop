# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

from accounts.views import *

class LoginPageTest(TestCase):

    def setUp(self):
        super(LoginPageTest, self).setUp()
        self.login_page = self.client.get('/account/login/')

    def test_login_page_resolves(self):
        login_page = resolve('/account/login/')
        self.assertEqual(login_page.func, login)

    def test_login_page_status_code_is_ok(self):
        self.assertEqual(self.login_page.status_code, 200)

    def test_login_page_uses_login_template(self):
        self.assertTemplateUsed(self.login_page, "accounts/login.html")


class AccountTest(TestCase):

    fixtures = ['accounts']

    def setUp(self):
        super(AccountTest, self).setUp()
        self.client.login(username='karla.slinton@example.com', password='karlas')
        self.account_page = self.client.get('/account/details/')

    def test_account_page_resolves(self):
        account_page = resolve('/account/details/')
        self.assertEqual(account_page.func, account)

    def test_account_page_status_code_is_ok(self):
        self.assertEqual(self.account_page.status_code, 200)

    def test_account_page_uses_account_template(self):
        self.assertTemplateUsed(self.account_page, "accounts/account.html")

    def test_account_page_content(self):
        user = User.objects.get(pk=16)
        address = Address.objects.get(user=user)
        account_page_template_output = render_to_response("accounts/account.html", {'address': address, 'user': user}).content
        self.assertEquals(self.account_page.content, account_page_template_output)


class LogoutTest(TestCase):

    fixtures = ['accounts']

    def test_logout(self):
        self.client.login(username='karla.slinton@example.com', password='karlas')
        response = self.client.get('/account/logout/')
        # check if user is redirected to another page
        self.assertEqual(response.status_code, 302)
        # check if user is redirected to homepage
        self.assertEqual(response['location'], '/')


class EditAddressTest(TestCase):

    fixtures = ['accounts']

    def setUp(self):
        super(EditAddressTest, self).setUp()
        self.user = User.objects.get(pk=16)
        self.client.login(username='karla.slinton@example.com', password='karlas')
        self.edit_address_page = self.client.get(reverse('edit_address', kwargs={'user_id': self.user.id}))

    def test_edit_address_page_resolves(self):
        edit_address_page = resolve(reverse('edit_address', kwargs={'user_id': self.user.id}))
        self.assertEqual(edit_address_page.func, edit_address)

    def test_edit_address_page_status_code_is_ok(self):
        self.assertEqual(self.edit_address_page.status_code, 200)

    def test_edit_address_page_uses_account_template(self):
        self.assertTemplateUsed(self.edit_address_page, "accounts/account_address_form.html")

    def test_edit_address_page_content(self):
        address = Address.objects.get(user=self.user)
        # check if address details are in the page content
        self.assertIn(str(address.house_number_name), self.edit_address_page.content)
        self.assertIn(str(address.street), self.edit_address_page.content)
        self.assertIn(str(address.town), self.edit_address_page.content)
        self.assertIn(str(address.postcode), self.edit_address_page.content)


class EditDetailsTest(TestCase):

    fixtures = ['accounts']

    def setUp(self):
        super(EditDetailsTest, self).setUp()
        self.user = User.objects.get(pk=16)
        self.client.login(username='karla.slinton@example.com', password='karlas')
        self.edit_details_page = self.client.get(reverse('edit_details', kwargs={'user_id': self.user.id}))

    def test_edit_details_page_resolves(self):
        edit_address_page = resolve(reverse('edit_details', kwargs={'user_id': self.user.id}))
        self.assertEqual(edit_address_page.func, edit_details)

    def test_edit_details_page_status_code_is_ok(self):
        self.assertEqual(self.edit_details_page.status_code, 200)

    def test_edit_details_page_uses_account_template(self):
        self.assertTemplateUsed(self.edit_details_page, "accounts/account_details_form.html")

    def test_edit_details_page_content(self):
        # check if user details are in the page content
        self.assertIn(str(self.user.first_name), self.edit_details_page.content)
        self.assertIn(str(self.user.last_name), self.edit_details_page.content)
        self.assertIn(str(self.user.email), self.edit_details_page.content)