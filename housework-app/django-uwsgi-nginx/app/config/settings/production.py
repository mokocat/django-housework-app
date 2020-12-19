from .base import *

LOG_HANDLER = ["todo"]

env = environ.Env(DEBUG=(bool, False))
env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# SECURITY SETTINGS
# security.W004
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# security.W008
SECURE_SSL_REDIRECT = True
# security.W012
SESSION_COOKIE_SECURE = True
# security.W016
CSRF_COOKIE_SECURE = True
# security.W022
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'

MEDIA_ROOT = '/usr/share/nginx/html/media'

LOGGING = {
    'version': 1,
    'formatters': {
        'todo': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        }
    },
    'handlers': {
        'todo': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/django/todo.log',
            'formatter': 'todo',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['todo'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['todo'],
            'level': 'INFO',
            'propagate': True,
        },
        'todo': {
            'handlers': LOG_HANDLER,
            'level': 'INFO',
            'propagate': True,
        },
    },
}
