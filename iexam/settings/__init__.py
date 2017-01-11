from .base import *

if 'SERVER_SOFTWARE' in os.environ:
	sae = True
	heroku = False
	mysql = False
else:
	sae = False
	heroku = False
	mysql = False


if mysql:
	from .mysql import *

if 'SERVER_SOFTWARE' in os.environ: 
	from .sae import *
elif sae:
	from .sae import *	
elif mysql:
	from .mysql import *
elif heroku:
	from .production import *
else:
	pass