import os
from django.conf import settings

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = settings.DATABASES

MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
MYSQL_PORT = '3307'
MYSQL_USER = 'ACCESSKEY'
MYSQL_PASS = 'SECRETKEY'
MYSQL_DB   = 'app_iexam'

#from sae._restful_mysql import monkey
#monkey.patch()

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST,
        'PORT':     MYSQL_PORT,
    }
}