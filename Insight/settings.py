from pathlib import Path

import dj_database_url

import environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.onrender.com', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "core",
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

ROOT_URLCONF = 'Insight.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL  = '/static/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'static_cdn')

TEMP_STATIC_ROOT = Path.joinpath(BASE_DIR, 'static')
MEDIA_URL   = '/media/'
MEDIA_ROOT  = Path.joinpath(BASE_DIR, 'static/media')

MODEL_PATH_FIELD_DIRECTORY = Path.joinpath(BASE_DIR, 'static/media/saved_models')

ADMIN_MEDIA_URL = STATIC_URL + 'admin/' #admin is now served by staticfiles

STATICFILES_DIRS = [
    Path.joinpath(BASE_DIR, 'static'),
    # Path.joinpath(BASE_DIR, '..', 'frontend', 'build', 'static'),
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"  # new


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

WSGI_APPLICATION = 'Insight.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

LIST_OF_DATABASES = {
    # local database
    'local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongo': {
        'ENGINE': 'djongo',
        'NAME': 'Insight',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': env('MONGO_CONNECTION_STRING')
        }  
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}

DATABASES = {
    'default': LIST_OF_DATABASES['postgres']
}



MEM_BASED_CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
FILE_BASED_CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'caches',
    }
}

CACHES = FILE_BASED_CACHE

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:3000"
# ]

# CORS_ORIGIN_WHITELIST = (
#     '127.0.0.1:3000',
# )

CORS_ALLOW_ALL_ORIGINS = True

WSGI_APPLICATION = 'Insight.wsgi.app'