from .base import *

sae = False
live = True
mysql = False

if live:
	from .production import *

if sae:
	from .sae import *

if mysql:
	from .mysql import *
