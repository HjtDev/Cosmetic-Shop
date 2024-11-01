"""
Django settings for CosmeticsShop project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os.path
from pathlib import Path
from django.contrib import admin
import locale

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1g%vt99#b+j*3yizn#2t-2!2nd9r7a-uek6k7yj*ljx4cf0sc4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Redirect all HTTP requests to HTTPS
SESSION_COOKIE_SECURE = False  # Ensure cookies are only sent over HTTPS
CSRF_COOKIE_SECURE = False  # Ensure CSRF cookies are only sent over HTTPS


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'product.apps.ProductConfig',
    'order.apps.OrderConfig',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'django_jalali',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CosmeticsShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'shop.context_processors.today',
                'shop.context_processors.header_products'
            ],
        },
    },
]

WSGI_APPLICATION = 'CosmeticsShop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oriflam1_db',
        'USER': 'oriflam1_db_user',
        'PASSWORD': 'hdf1jsE$FF$#g124',
    }
}

DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'cosmetics_shop',
#    }
#}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

#locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
# MEDIA_ROOT = '/home/oriflam1/public_html/media/'
MEDIA_ROOT = BASE_DIR / 'media'
#MEDIA_ROOT = '/home/oriflam1/pulbic_html/media/'

#DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 Mb

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

JAZZMIN_SETTINGS = {
    'custom_css': 'css/admin.css'
}


admin.sites.AdminSite.site_header = 'پنل مدیریت'
admin.sites.AdminSite.site_title = 'فروشگاه'
admin.sites.AdminSite.index_title = 'پنل مدیریت'


SESSION_COOKIE_AGE = 86400  # 24 Hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
# DJANGORESIZED_DEFAULT_SCALE = 0.5
DJANGORESIZED_DEFAULT_QUALITY = 100
# DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'PNG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'WEBP': ".webp",
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = False


LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'
LOGIN_REDIRECT_URL = 'account:profile'
LOGOUT_REDIRECT_URL = 'account:login'
