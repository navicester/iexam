
import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, '..', 'site-packages'))

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__) 
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.stdout = sys.stderr
sys.path.append(project)
#sys.path.append(workspace)

os.environ['DJANGO_SETTINGS_MODULE'] = "iexam.settings"

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
