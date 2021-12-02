from os import path, environ

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'test_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongo'
        }
    }
}

BASEDIR = path.dirname(path.abspath(__file__))

STORE_NAME = 'WStore'
AUTH_PROFILE_MODULE = 'wstore.models.UserProfile'

ADMIN_ROLE = 'admin'
PROVIDER_ROLE = 'seller'
CUSTOMER_ROLE = 'customer'

LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_DIR = 'media/'
MEDIA_ROOT = path.join(BASEDIR, MEDIA_DIR)
BILL_ROOT = path.join(MEDIA_ROOT, 'bills')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/charging/media/'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    #'django.contrib.admin',
    #'wstore.store_commons',
    'wstore',
    #'wstore.charging_engine',
    #'django_crontab',
    #'django_nose'
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8p509oqr^68+z)y48_*pv!ceun)gu7)yw6%y9j2^0=o14)jetr'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

WSTOREMAILUSER = 'email_user'
WSTOREMAIL = 'wstore@email.com'
WSTOREMAILPASS = 'wstore_email_passwd'
SMTPSERVER = 'wstore_smtp_server'
SMTPPORT = 587


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'wstore.store_commons.middleware.AuthenticationMiddleware'
]

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

# Payment method determines the payment gateway to be used
# Allowed values: paypal (default), fipay, None
PAYMENT_METHOD = 'paypal'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Daily job that checks pending pay-per-use charges
CRONJOBS = [
    ('0 5 * * *', 'django.core.management.call_command', ['pending_charges_daemon']),
    ('0 6 * * *', 'django.core.management.call_command', ['resend_cdrs']),
    ('0 4 * * *', 'django.core.management.call_command', ['resend_upgrade'])
]

CLIENTS = {
    'paypal': 'wstore.charging_engine.payment_client.paypal_client.PayPalClient',
    'fipay': 'wstore.charging_engine.payment_client.fipay_client.FiPayClient',
    None: 'wstore.charging_engine.payment_client.payment_client.PaymentClient'
}

NOTIF_CERT_FILE = None
NOTIF_CERT_KEY_FILE = None

PROPAGATE_TOKEN = True

from services_settings import *
