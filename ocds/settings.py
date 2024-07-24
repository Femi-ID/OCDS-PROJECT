"""
Django settings for ocds project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')
# DEBUG = True

# ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(" ")
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")
# ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # added dependencies
    'rest_framework',
    'taggit',
    'djoser',
    # 'rest_framework.authtoken',
    'corsheaders',

    # applications
    'accounts',
    'questions',
]

AUTH_USER_MODEL = 'accounts.User'

# Django Taggit settings
# TAGGIT_CASE_INSENSITIVE = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


ROOT_URLCONF = 'ocds.urls'

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

WSGI_APPLICATION = 'ocds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '', 
        'PORT': '',
    },

    # 'default': dj_database_url.config(
    #     # Replace this value with your local database's connection string.
    #     default='postgresql://postgres:postgres@localhost:5432/mysite',
    #     conn_max_age=600
    # )
}

# postgres://USER:PASSWORD@INTERNAL_HOST:PORT/DATABASE
# database_url = config("DATABASE_URL")
database_url = os.environ.get("DATABASE_URL")
DATABASES['default'] = dj_database_url.parse('postgresql://ocds_team:lnr7eWhNLar0bQllFsUtsTZtPrIysn0q@dpg-cqgeak56l47c73bu0hd0-a/ocds_db_bcfs')


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
# RAILWAY CONFIG
# STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True # consider this during production
CORS_ALLOWED_ORIGINS = [
    '127.0.0.1:8000', 'https://ocds-project.onrender.com', 
]

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEYS": "errors",

    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    "DEFAULT_PERMISSIONS_CLASSES": (
        'rest-framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'), # To be added in auth header {"Bearer": access token}
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3)
}

DJOSER = {
    'LOGIN_FIELD': 'email',

    # sign up user
    'SEND_ACTIVATION_EMAIL': True, # instance: account creation, email update
    'SEND_CONFIRMATION_EMAIL': True, # sent after account activation
    'USER_CREATE_PASSWORD_RETYPE': True, # ensure a confirm password field on user creation
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # When clicked in the email it sends a post request to the activation endpoint with uid and token arguments
    'ACTIVATION_URL': 'auth/users/activate/{uid}/{token}', # link to be sent to the email
    'PASSWORD_RESET_CONFIRM_URL': 'auth/reset-password/?uid={uid}&token={token}',

    # new password
    'SET_PASSWORD_RETYPE': True,

    'SERIALIZERS': {
        # create new user
        'user_create': 'accounts.serializers.UserCreateSerializer',
        'user_create': 'djoser.urls',

        # view for users list and current user profile 
        'user': 'accounts.serializers.UserSerializer',
        'current_user': 'accounts.serializers.UserSerializer',

        # password reset confirmation
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',

        # token view
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
}

# The name that will be used in the activation email
SITE_NAME = 'OCDS PROJECT'
DOMAIN = 'ocds-project.onrender.com'
# The ACTIVATION_URL will be appended to the domain and sent to the user's email
# The link routes to the frontend (react view) and sends the request to the server
# Same applies for 'PASSWORD_RESET_CONFIRM_URL'
 


# Email Config
# EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_PORT = config('EMAIL_PORT')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS')
# DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')
# MAILER_EMAIL_BACKEND = config('MAILER_EMAIL_BACKEND')


EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')


if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
