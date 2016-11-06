from .base import *

sae = True
heroku = False
mysql = False

if heroku:
	from .production import *

if sae:
	from .sae import *

if mysql:
	from .mysql import *
