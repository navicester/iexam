import os
from django.conf import settings

#DEBUG = False
#TEMPLATE_DEBUG = False

DATABASES = settings.DATABASES

MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
MYSQL_PORT = '3307'
MYSQL_USER = 'xw4o0y0lj1' #ACCESSKEY
MYSQL_PASS = 'jx2kzh220z1iwl34l51y3jlxm4k5i5ji0mhxki3w' #SECRETKEY
MYSQL_DB   = 'app_iexam'

from sae._restful_mysql import monkey
monkey.patch()

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