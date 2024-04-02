# myproject/settings.py
import os
from pathlib import Path
import re
from celery.schedules import crontab
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ''

DEBUG = True

ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = True


INSTALLED_APPS = [
    'myapp',
    'corsheaders',  # обязательно добавьте это приложение
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_extensions',
    'axes',
]

MIDDLEWARE = [
		'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
    #'myproject.restrict_ip_middleware.AllowIPMiddleware',
    'axes.middleware.AxesMiddleware',
]

CORS_ALLOWED_ORIGIN_REGEXES = [

]

CORS_URLS_REGEX = r'^/your_post_endpoint/'

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'myapp/static'

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_CREDENTIALS = True


CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BEAT_SCHEDULE = {
    'send-greetings-every-day': {
        'task': 'myapp.tasks.send_greetings',
        'schedule': crontab(hour=12, minute=14),
    },
}

LOGIN_URL = 'login'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }

# Настройки сессии
SESSION_COOKIE_AGE = 15 
SESSION_SAVE_EVERY_REQUEST = True 
SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_HTTPONLY = True 
SECURE_SESSION_COOKIE = True  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  


AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  	
    'django.contrib.auth.backends.ModelBackend',
]


AXES_FAILURE_LIMIT = 3 
AXES_COOLOFF_TIME = 24 
AXES_LOCKOUT_TEMPLATE = 'lockout.html'  
