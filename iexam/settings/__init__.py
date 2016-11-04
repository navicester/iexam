from .base import *

sae = False
live = False

if live:
	from .production import *

if sae:
	from .sae import *
	
# print STATIC_ROOT
# print DATABASES['default']
