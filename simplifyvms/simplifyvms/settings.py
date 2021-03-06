"""
Django settings for simplifyvms project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
import yaml
import json
import logging.config
from pathlib import Path

APP_ENV = os.environ.get('APP_ENV', "LOCAL")

# loading configuration from settings.yaml file
SETTINGS_YML_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'settings.yaml')

with open(SETTINGS_YML_FILE, 'r') as f:
    config_contents = yaml.load(f, Loader=yaml.FullLoader)
    CONFIG = config_contents["DEFAULT"]
    CONFIG.update(config_contents[APP_ENV])

# if APP_ENV != 'LOCAL':

#     # get secret from the aws secret managers
#     secret_var = get_secret(
#         CONFIG["AWS"]["AWS_SECRET_NAME"], CONFIG["AWS"]["AWS_REGION"])
#     secret_var = json.loads(secret_var)
#     CONFIG.update(secret_var)


# setup logging
PROFILE_ENDPOINT = CONFIG['PROFILE_ENDPOINT']
HIRARCHY_ROLE_ENDPOINT = CONFIG['HIRARCHY_ROLE_ENDPOINT']
SENDER_ENDPOINT = CONFIG['SENDER_ENDPOINT']
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(levelname)-1s: %(asctime)s\
                      [%(name)-12s.%(funcName)s] %(message)s',
        },
        'file': {
            'format': '%(levelname)-1s: %(asctime)s\
                      [%(name)-12s.%(funcName)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': CONFIG["LOGGING"]["HANDLERS_CONSOLE_LEVEL"],
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': sys.stdout
        },
        'file': {
            'level': CONFIG["LOGGING"]["HANDLERS_CONSOLE_LEVEL"],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': 'logs/approval_logs.log',
        },
    },
    'loggers': {
        '': {
            'handlers': [CONFIG['LOGGING_HANDLER']],
            'level': CONFIG["LOGGING"]["LOGGERS_DEFAULT_LEVEL"],
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG["DEBUG"]

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # rest_framework
    'rest_framework',

    'django_filters',

    # stomp client
    'django_stomp',
]

INSTALLED_APPS += [
    'approval_engine',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simplifyvms.urls'

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

WSGI_APPLICATION = 'simplifyvms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

CONFIG["DATABASES"]['default']['CONN_MAX_AGE'] = 390
DATABASES = CONFIG["DATABASES"]


# Rest Framework
REST_FRAMEWORK = CONFIG["REST_FRAMEWORK"]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = CONFIG['STATIC_URL']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STOMP Configurations
STOMP_SERVER_HOST = CONFIG["STOMP"]["SERVER_HOST"]
STOMP_SERVER_PORT = CONFIG["STOMP"]["SERVER_PORT"]
STOMP_USE_SSL = CONFIG["STOMP"]["USE_SSL"]
STOMP_CORRELATION_ID_REQUIRED = CONFIG["STOMP"]["CORRELATION_ID_REQUIRED"]
STOMP_PROCESS_MSG_ON_BACKGROUND = CONFIG["STOMP"]["PROCESS_MSG_ON_BACKGROUND"]
STOMP_SERVER_USER = CONFIG["STOMP"]["USERNAME"]
STOMP_SERVER_PASSWORD = CONFIG["STOMP"]["PASSWORD"]


