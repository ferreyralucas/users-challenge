import sys

import django
from django.utils.encoding import force_str, smart_str

import environ

"""
TEMPORAL FIX POR DJANGO > 4.0
THERE IS AN ERROR RUNNING THE COLLECTION STATIC PIPELINE BECAUSE IT GIVES THE FOLLOWING ERRORS
ImportError: cannot import name 'force_text' from 'django.utils.encoding'
ImportError: cannot import name 'smart_text' from 'django.utils.encoding'
IN DJANGO 4 THE FORCE_TEXT AND SMART_TEXT METHOD WERE REMOVED
https://docs.djangoproject.com/en/4.0/releases/4.0/#features-removed-in-4-0
THE PROBLEM IS THAT THERE ARE LIBRARIES THAT STILL USE THOSE METHODS SO WE HAVE TO ADD THIS FIX
"""
# ------------------- START OF FIX
django.utils.encoding.force_text = force_str
django.utils.encoding.smart_text = smart_str
# ------------------- END OF FIX


ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('apps')

env = environ.Env()

ENVIRONMENT = env('ENVIRONMENT')

env.read_env(str(ROOT_DIR.path('.env')))

if ENVIRONMENT == 'test':
    env.read_env(str(ROOT_DIR.path('env.test')))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, ROOT_DIR('apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')


ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", [])
CSRF_TRUSTED_ORIGINS = ['https://*']


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'rest_framework_simplejwt',
]

LOCAL_APPS = [
    'apps.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# # DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL')
}


# # PASSWORD VALIDATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
    {
        'NAME': 'users.validators.UppercaseLowercaseNumbersSymbolsValidator',
    },
]


# # INTERNATIONALIZATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Buenos_Aires'
USE_I18N = True
USE_TZ = True


# # STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = '/static/'
STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# # MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'


# # DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
# # CORS APP
# ------------------------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

# AUTHENTICATION
AUTH_USER_MODEL = 'users.User'


SUBSCRIPTION_SERVICE_MOCK = env.bool('SUBSCRIPTION_SERVICE_MOCK')
