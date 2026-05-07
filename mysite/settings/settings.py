

from pathlib import Path
from datetime  import timedelta 

import os 


from decouple import config, Csv
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY =config("SECRET_KEY")




DEBUG = config("DEBUG", cast=bool,default=False)


ALLOWED_HOSTS = ['hr-system-99ym.onrender.com','127.0.0.1']




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'silk',
    'employee_module',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    "corsheaders",
    "django_filters",
    'task',
    'attendance_module',
    'django_celery_results',
    'django_celery_beat',
    'leave_module',
    'drf_spectacular_sidecar',
    'drf_spectacular',
    'payroll_module',
    'analytics_module',
    'sod_eod_module'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('DATABASE_NAME'),
        "USER": config('DATABASE_USER'),
        "PASSWORD": config('DATABASE_PASSWORD'),
        "HOST": config('DATABASE_HOST'),
        "PORT": '5432',
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

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


CSRF_TRUSTED_ORIGINS = [
    'https://hr-system-99ym.onrender.com',
    'http://localhost:3000',  
    'http://127.0.0.1:3000',  
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    
    "http://127.0.0.1:3000",
    "https://hr-system-99ym.onrender.com", 
]
STATIC_URL = 'static/'
STATIC_ROOT=BASE_DIR/'static'

MEDIA_URL='media/'
MEDIA_ROOT=BASE_DIR/'media'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", 
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    
    "http://127.0.0.1:3000",
   
]
CORS_ALLOW_CREDENTIALS = True

CELERY_BROKER_URL = "redis://redis:6379/0"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kathmandu"
CELERY_ENABLE_UTC = True
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_RESULT_BACKEND = 'django-db'