

import os
import sys
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE" , "iexam.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ["Hello,  django! version: " + str(django.VERSION)]

#import sae
#from iexam import wsgi
#application = sae.create_wsgi_app(wsgi.application)
#application = sae.create_wsgi_app(app)