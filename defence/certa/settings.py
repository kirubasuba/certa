"""
Django settings for certa project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mfbfrzdbx4yz0t3=g_wqspy18%0v-s60#t!-r_75+*d_8tt5j!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'common.apps.CommonConfig',
    'authmgmt.apps.AuthmgmtConfig',
    'dashboard.apps.DashboardConfig',
    'crispy_forms',
    'bootstrap_modal_forms',
 ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'certa.middleware.authmiddleware.AuthenticationRequiredMiddleware',
]


ROOT_URLCONF = 'certa.urls'

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

WSGI_APPLICATION = 'certa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'djongo',
        # 'NAME': 'etadmdevdb',
        # 'HOST':'mongodb://localhost:27017/etadmdevdb'

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tadmsnew',
        'USER':'postgres',
        'PASSWORD':'postgres',
        'HOST':'localhost'
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL='/auth/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 25
EMAIL_HOST = 'smtp.cemilac.com'
EMAIL_HOST_USER = 'kiruba@cemilac.com'
EMAIL_HOST_PASSWORD = '12345'
EMAIL_USE_TLS = True
SESSION_COOKIE_AGE=10


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'kiruba@gennext.com'
# EMAIL_HOST = 'smtp.gennext.com'

# # Port for sending e-mail.
# EMAIL_PORT = 25

# # Optional SMTP authentication information for EMAIL_HOST.
# EMAIL_HOST_USER = 'kiruba@gennext.com'
# EMAIL_HOST_PASSWORD = 'sublee@123'
# EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_PORT = 25
# EMAIL_HOST = 'smtp.cemilac.com'
# EMAIL_HOST_USER = 'admin@cemilac.com'
# EMAIL_HOST_PASSWORD = '12345'
# EMAIL_USE_TLS = True
# SESSION_COOKIE_AGE=10