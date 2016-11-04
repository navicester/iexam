from .base import *

sae = False
live = False
mysql = True

if live:
	from .production import *

if sae:
	from .sae import *

if mysql:
	from .mysql import *
