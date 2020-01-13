# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2018 CoNWeT Lab., Universidad Politécnica de Madrid
# Copyright (c) 2019 Future Internet Consulting and Development Solutions S.L.

# This file belongs to the business-ecosystem-charging-backend
# of the Business API Ecosystem.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_DIR = 'media/'
MEDIA_ROOT = path.join(BASEDIR, MEDIA_DIR)
BILL_ROOT = path.join(MEDIA_ROOT, 'bills')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/charging/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ghr40bk7aq1@sxwjffm&763)yd&1&%2srtf2$q6$srhoz*zn)#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

STORE_NAME = 'WStore'
AUTH_PROFILE_MODULE = 'wstore.models.UserProfile'

ADMIN_ROLE = 'admin'
PROVIDER_ROLE = 'seller'
CUSTOMER_ROLE = 'customer'

CHARGE_PERIODS = {
    'daily': 1,  # One day
    'weekly': 7,  # One week
    'monthly': 30,  # One month
    'quarterly': 90,  # Three months
    'yearly': 365,  # One year
    'quinquennial': 1825,  # Five years
}

CURRENCY_CODES = [
    ('AUD', 'Australia Dollar'),
    ('BRL', 'Brazil Real'),
    ('CAD', 'Canada Dollar'),
    ('CHF', 'Switzerland Franc'),
    ('CZK', 'Czech Republic Koruna'),
    ('DKK', 'Denmark Krone'),
    ('EUR', 'Euro'),
    ('GBP', 'United Kingdom Pound'),
    ('HKD', 'Hong Kong Dollar'),
    ('HUF', 'Hungary Forint'),
    ('ILS', 'Israel Shekel'),
    ('JPY', 'Japan Yen'),
    ('MXN', 'Mexico Peso'),
    ('MYR', 'Malaysia Ringgit'),
    ('NOK', 'Norway Krone'),
    ('NZD', 'New Zealand Dollar'),
    ('PHP', 'Philippines Peso'),
    ('PLN', 'Poland Zloty'),
    ('RUB', 'Russia Ruble'),
    ('SEK', 'Sweden Krona'),
    ('SGD', 'Singapore Dollar'),
    ('THB', 'Thailand Baht'),
    ('TRY', 'Turkey Lira'),
    ('TWD', 'Taiwan New Dollar'),
    ('USD', 'US Dollar'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wstore',
    'django_crontab',
    'django_nose'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'wstore.store_commons.middleware.AuthenticationMiddleware'
]

ROOT_URLCONF = 'wstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

PAYMENT_METHOD = 'paypal'

CLIENTS = {
    'paypal': 'wstore.charging_engine.payment_client.paypal_client.PayPalClient',
    'fipay': 'wstore.charging_engine.payment_client.fipay_client.FiPayClient',
    None: 'wstore.charging_engine.payment_client.payment_client.PaymentClient'
}

WSTOREMAILUSER = 'email_user'
WSTOREMAIL = 'wstore@email.com'
WSTOREMAILPASS = 'wstore_email_passwd'
SMTPSERVER = 'wstore_smtp_server'
SMTPPORT = 587

NOTIF_CERT_FILE = None
NOTIF_CERT_KEY_FILE = None

from services_settings import *

# =====================================
# ENVIRONMENT SETTINGS
# =====================================

DATABASES['default']['NAME'] = environ.get('BAE_CB_MONGO_DB', DATABASES['default']['NAME'])
DATABASES['default']['USER'] = environ.get('BAE_CB_MONGO_USER', DATABASES['default']['USER'])
DATABASES['default']['PASSWORD'] = environ.get('BAE_CB_MONGO_PASS', DATABASES['default']['PASSWORD'])
DATABASES['default']['HOST'] = environ.get('BAE_CB_MONGO_SERVER', DATABASES['default']['HOST'])
DATABASES['default']['PORT'] = environ.get('BAE_CB_MONGO_PORT', DATABASES['default']['PORT'])

ADMIN_ROLE = environ.get('BAE_LP_OAUTH2_ADMIN_ROLE', ADMIN_ROLE)
PROVIDER_ROLE = environ.get('BAE_LP_OAUTH2_SELLER_ROLE', PROVIDER_ROLE)
CUSTOMER_ROLE = environ.get('BAE_LP_OAUTH2_CUSTOMER_ROLE', CUSTOMER_ROLE)

WSTOREMAILUSER = environ.get('BAE_CB_EMAIL_USER', WSTOREMAILUSER)
WSTOREMAIL = environ.get('BAE_CB_EMAIL', WSTOREMAIL)
WSTOREMAILPASS = environ.get('BAE_CB_EMAIL_PASS', WSTOREMAILPASS)
SMTPSERVER = environ.get('BAE_CB_EMAIL_SMTP_SERVER', SMTPSERVER)
SMTPPORT = environ.get('BAE_CB_EMAIL_SMTP_PORT', SMTPPORT)

PAYMENT_METHOD = environ.get('BAE_CB_PAYMENT_METHOD', PAYMENT_METHOD)

if PAYMENT_METHOD == 'None':
    PAYMENT_METHOD = None

VERIFY_REQUESTS = environ.get('BAE_CB_VERIFY_REQUESTS', VERIFY_REQUESTS)
if isinstance(VERIFY_REQUESTS, str) or isinstance(VERIFY_REQUESTS, str):
    VERIFY_REQUESTS = VERIFY_REQUESTS == 'True'

SITE = environ.get('BAE_SERVICE_HOST', SITE)
LOCAL_SITE = environ.get('BAE_CB_LOCAL_SITE', LOCAL_SITE)

CATALOG = environ.get('BAE_CB_CATALOG', CATALOG)
INVENTORY = environ.get('BAE_CB_INVENTORY', INVENTORY)
ORDERING = environ.get('BAE_CB_ORDERING', ORDERING)
BILLING = environ.get('BAE_CB_BILLING', BILLING)
RSS = environ.get('BAE_CB_RSS', RSS)
USAGE = environ.get('BAE_CB_USAGE', USAGE)
AUTHORIZE_SERVICE = environ.get('BAE_CB_AUTHORIZE_SERVICE', AUTHORIZE_SERVICE)

PAYMENT_CLIENT = CLIENTS[PAYMENT_METHOD]
