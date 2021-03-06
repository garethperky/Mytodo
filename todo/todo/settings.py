"""
Django settings for todo project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json
import os

import boto3
from botocore.exceptions import ClientError
from django.urls import reverse_lazy


def get_secret(secret_name):
    endpoint_url = "https://secretsmanager.eu-west-2.amazonaws.com"
    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise RuntimeError(
                "The requested AWS secret " + secret_name + " was not found"
            )
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise RuntimeError("The AWS IAM request was invalid due to:", e)
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise RuntimeError("The AWS IAM request had invalid params:", e)
        else:
            raise RuntimeError(
                "Check AWS IAM permissions. Did you set DEBUG=true in your environment "
                + "if you are using development secrets?"
            )
    else:
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)


_SECRET = get_secret("mytestsite-secrets")

PUSH_OVER_APP_TOKEN = _SECRET["PUSH_OVER_APP_TOKEN"]
PUSH_OVER_USER_TOKEN = _SECRET["PUSH_OVER_USER_TOKEN"]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _SECRET["SECRET_KEY"]
AWS_ACCESS_KEY_ID = _SECRET["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = _SECRET["S3_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = _SECRET["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "3.8.143.185"]

DATE_INPUT_FORMATS = "%m/%d/%Y"

# Application definition

INSTALLED_APPS = [
    "todonow",
    'bootstrap4',
    "storages",
    "tempus_dominus",
    'django_extensions',
    'crispy_forms',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "todo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "todo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": _SECRET["DB_NAME"],
        "USER": _SECRET["DB_USER"],
        "PASSWORD": _SECRET["DB_PASSWORD"],
        "HOST": _SECRET["DB_HOST"],
        "PORT": _SECRET["DB_PORT"],
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-GB"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
LOGIN_REDIRECT_URL = reverse_lazy("index")
LOGOUT_REDIRECT_URL = reverse_lazy("index")
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = 'todo.storage_backends.MediaStorage'
STATIC_ROOT = os.path.join(BASE_DIR, "static_generated")
