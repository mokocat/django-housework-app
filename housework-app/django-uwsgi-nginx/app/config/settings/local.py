from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# This secret key is published for test, then you cannot use in production environment.
SECRET_KEY = 't@vl8u$$uirv_omcs*uo6o%3%1^!t_8*1l*%n=me6r+ox-l5+6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')