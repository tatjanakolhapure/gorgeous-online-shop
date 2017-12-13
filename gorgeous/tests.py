# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

from .views import contact

class ContactPageTest(TestCase):

    def setUp(self):
        super(ContactPageTest, self).setUp()
        self.contact_page = self.client.get('/contact/')

    def test_contact_page_resolves(self):
        contact_page = resolve('/contact/')
        self.assertEqual(contact_page.func, contact)

    def test_contact_page_status_code_is_ok(self):
        self.assertEqual(self.contact_page.status_code, 200)

    def test_contact_page_uses_correct_template(self):
        self.assertTemplateUsed(self.contact_page, "contact.html")

    def test_contact_page_content(self):
        contact_page_template_output = render_to_response("contact.html").content
        self.assertEquals(self.contact_page.content, contact_page_template_output)