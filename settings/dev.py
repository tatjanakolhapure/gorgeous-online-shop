from base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_oV4e35Zirwo0wmm7ZrjgZO1k')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_wUTLcpVb8nhWmDxUhBKd0Yxc')