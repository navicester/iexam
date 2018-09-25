 # -*- coding: utf-8 -*-

"""
Django settings for iexam project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #add settings as dedicated folder

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u(+p48v^a25q!d6lrc3oou)_%v%xwj^xc*)5f_t=(iefi278m('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    ('countrysidedog', 'csdog@countrysidedog.com'),
)

# Application definition

INSTALLED_APPS = (
    #'grappelli', # must before admin
    #'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'breadcrumbs',
    'plugin',
    'pagination',
    'newsletter',
    'exam',
    'engdict',
    'crispy_forms',
    'registration',
    'adminextend',    
    'iexam'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',    
    'iexam.middleware.ForceDefaultLanguageMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'iexam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), 
                        os.path.join(BASE_DIR, "exam", "templates"), 
                        os.path.join(BASE_DIR, "engdict", "templates"), 
                        os.path.join(BASE_DIR, "adminextend", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.i18n",
                #'django.core.context_processors.request', # add for suit
            ],
        },
    },
]

WSGI_APPLICATION = 'iexam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import socket

DB_SQLITE = False    
DB_MYSQL = False

if os.getenv('DJANGO_SQL_SERVER'):
    DB_MYSQL = True
    MEDIA_PREFIX = "DB_SQL_" + socket.gethostname()
else:
    DB_SQLITE = True
    MEDIA_PREFIX = "DB_SQLITE"

if socket.gethostname() == "PC-20130414CBMY":
    DB_MYSQL = False

if DB_MYSQL:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     'iexam',
            'USER':     'root',
            'PASSWORD': '123',
            'HOST':     '',
            'PORT':     '',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True




LANGUAGES = (
    ('en-us', ('English')),
    ('zh-cn', ('中文简体')),
    ('zh-tw', ('中文繁體')),
)
'''
ugettext = lambda s: s
LANGUAGES = (
    ('en-us', ugettext('English')),
    ('zh-cn', ugettext('Chinese Simple')),
    ('zh-tw', ugettext('Chinese taiwan')),
)
'''

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")
STATIC_ROOT = os.path.join(BASE_DIR, "static_in_env", "static_root")

STATICFILES_DIRS = (        
    os.path.join(BASE_DIR, "adminextend", "static"),
    #os.path.join(BASE_DIR, "static_in_pro", "admin_static"), # href="{% static "admin/css/changelists.css" %}"
    os.path.join(BASE_DIR, "static_in_pro", "our_static"),
    #os.path.join(BASE_DIR, "site-packages","django","contrib","static"),
    
    #'/var/www/static/',
)

MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")
MEDIA_ROOT = os.path.join(BASE_DIR, "static_in_env", "media_root")

# print "base dir" + BASE_DIR
# print "STATIC_ROOT" + STATIC_ROOT
# print STATICFILES_DIRS

try:
    import settings_security
    EMAIL_HOST_USER = settings_security.USER_NAME
    EMAIL_HOST_PASSWORD = settings_security.USER_PWD
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
except:
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''

EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

'''
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25

EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
'''




#Crispy FORM TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#DJANGO REGISTRATION REDUX SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
REGISTRATION_EMAIL_SUBJECT_PREFIX = '[Django Registration iexam]'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SEND_ACTIVATION_EMAIL = True

#ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"  

'''
SUIT_CONFIG = {
    'ADMIN_NAME': 'HSSE',
    # each dict represent one column on left side
    # label mean name, app mean the app installed above, models means model used
    
    #'MENU': ({'label': 'engdict',
    #          'app': 'engdict',
    #          'models': ('word',)},
    #         ),
}
'''

import re

MARKDOWN_DEUX_STYLES = {
    # "default": MARKDOWN_DEUX_DEFAULT_STYLE,
    "trusted": {
        "extras": {
            "code-friendly": None,
        },
        # Allow raw HTML (WARNING: don't use this for user-generated
        # Markdown for your site!).
        "safe_mode": False,
    },
    # Here is what http://code.activestate.com/recipes/ currently uses.
    "recipe": {
        # "extras": {
        #     "code-friendly": None,
        # },
        # "safe_mode": "escape",
        "link_patterns": [
            # Transform "Recipe 123" in a link.
            (re.compile(r"recipe\s+#?(\d+)\b", re.I),
             r"http://code.activestate.com/recipes/\1/"),
        ],
        "extras": {
            "code-friendly": None,
            "pyshell": None,
            "demote-headers": 3,
            "link-patterns": None,
            # `class` attribute put on `pre` tags to enable using
            # <http://code.google.com/p/google-code-prettify/> for syntax
            # highlighting.
            "html-classes": {"pre": "prettyprint"},
            "cuddled-lists": None,
            "footnotes": None,
            "header-ids": None,
            # "fenced-code-blocks" : {'cssclass': 'mycodehilite', "prestyles":"background-color: #d2dee8;"},
            "fenced-code-blocks" : {'cssclass': 'mycodehilite',},
        },
        "safe_mode": "escape",

    }
}