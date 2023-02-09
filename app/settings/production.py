from .base import *

DEBUG = False

ALLOWED_HOSTS = ['zygmuntd.eu.pythonanywhere.com', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/home/zygmuntd/mysql.cnf',
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
