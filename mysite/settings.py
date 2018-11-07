"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jo^w72-vcqpxc%$4pviso1le-0mnj3o((-1*n&k2z+5s5a53z8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost',
                 '127.0.0.1',
                 '188.166.157.234',
                 'adm.brandfi.co.ke']


# Application definition

INSTALLED_APPS = [
    'ads.apps.AdsConfig',
    'splashads.apps.SplashadsConfig',
    'corsheaders',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'radius',
        'USER': 'fatjoe',
        'PASSWORD': 'Darthvader_89',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

ADS_ZONES = {
    'header': {
        'name': ('Header'),
        'ad_size': {
            'xs': '274x150',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
    },
    'content': {
        'name': ('Content'),
        'ad_size': {
            'xs': '274x202',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
    },
    'sidebar': {
        'name': ('Sidebar'),
        'ad_size': {
            'xs': '274x104',
            'sm': '800x90',
            'md': '800x90',
            'lg': '800x90'
        },
    },
}

ADS_DEFAULT_AD_SIZE = '720x150'

ADS_DEVICES = (
    ('xs', ('Smartphones')),
    ('sm', ('Tablets')),
    ('md', ('Small Desktops')),
    ('lg', ('Large Desktops'))
)


CORS_ORIGIN_ALLOW_ALL = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 20 * 60

# SESSION_IDLE_TIMEOUT = 2 * 60
