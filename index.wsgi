import sae
from iexam import wsgi

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ["Hello,  django! version: " + str(django.VERSION)]
	
#application = sae.create_wsgi_app(wsgi.application)
application = sae.create_wsgi_app(app)