"""
Django settings for antiguos_alumnos_tfg project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#'C:\\Users\\carlo\\Documents\\Carlos Mata Blasco\\Universidad\\Django\\antiguos_alumnos_tfg'
#'C:/Users/carlo/Documents/Carlos Mata Blasco/Universidad/Django/antiguos_alumnos_tfg/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm5_+&)(d0$x+b0ow78g9wh)16buct811dv8n!(&lhbxr363f)%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'mathfilters',
    'gestionBD',
]

#AUTHENTICATION_BACKENDS = [
#    'social_core.backends.twitter.TwitterOAuth',
#]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'antiguos_alumnos_tfg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'antiguos_alumnos_tfg/templates')],
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

WSGI_APPLICATION = 'antiguos_alumnos_tfg.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'antiguosalumnos',
        'USER': 'postgres',
        'PASSWORD': 'postgresql',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

#C:/Users/carlo/Documents/Carlos Mata Blasco/Universidad/Django/antiguos_alumnos_tfg/antiguos_alumnos_tfg/static/
#<link rel="shortcut icon" href="{% static 'images/antalumnos_icono.ico' %}" />

DATE_INPUT_FORMATS = ['%d/%m/%Y']


# Static files:
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = ["C:/Users/carlo/Documents/Carlos Mata Blasco/Universidad/Django/antiguos_alumnos_tfg/antiguos_alumnos_tfg/static/"]


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#MEDIA_URL = '/static/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'antiguos_alumnos_tfg/multimedia')


# Gmail:
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "antalumnosetsi@gmail.com"
EMAIL_HOST_PASSWORD = "Admintfg20"


# Twitter:
TWITTER_API_KEY = 'XSPvc9U4HgUm2dfqoY9WBvtHI'
TWITTER_API_SECRET_KEY = 'manhSe3L3mnjKHQjMu3QtUtDBQSlqX29217dyjB7FA6gE4THT4'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHY3NAEAAAAASx0C2kbj6aTFKgSisgu%2FYWt3csc%3D13acJHT3ei9RarsWuOfv4PvSjCqP4NdIR1NsqQ2hI6A0oKkl53'
TWITTER_ACCESS_TOKEN = '1327583260348739590-6uTs3sucXoMRV4UyIJ0Tr2EdhOiSR0'
TWITTER_ACCESS_TOKEN_SECRET = 'YHlo610QHMmU5cE7CVDAfR1GeAmWcbyuHvdcAPyONUP7O'