
import os
import sys

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)  #e:\PythonWeb\code\voith_sales\Rail\apache_django_wsgi.conf
project = os.path.dirname(apache_configuration)  #e:\PythonWeb\code\voith_sales\Rail
workspace = os.path.dirname(project) #e:\PythonWeb\code\voith_sales
sys.stdout = sys.stderr
sys.path.append(workspace)

print workspace


os.environ['DJANGO_SETTINGS_MODULE'] = "iexam.iexam.settings"
#import django
#django.setup()
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()