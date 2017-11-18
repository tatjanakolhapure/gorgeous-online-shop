# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
from django.db import models
from django.conf import settings

class AccountUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email, is_active=True,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    objects = AccountUserManager()
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    house_number_name = models.CharField("House number/name", max_length=40)
    street = models.CharField(max_length=40)
    town = models.CharField(max_length=40)
    postcode = models.CharField(max_length=10)