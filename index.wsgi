import sae
from iexam import wsgi

application = sae.create_wsgi_app(wsgi.application)