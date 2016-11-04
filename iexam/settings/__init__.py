from .base import *

sae = True
live = False
mysql = False

if live:
	from .production import *

if sae:
	from .sae import *

if mysql:
	from .mysql import *
