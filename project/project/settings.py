import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gsh+ih2q-g0l-z)2f_7&#odg4k$-k-)rtmg#%x7v28vpd&5&wa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
     # встроенное прил. Django, которое добавляет пользователей
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # встроенное прил. Django, которое добавляет сообщения
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # встроенное прил. Django, которое добавляет настройки сайта
    'django.contrib.sites',
    'django.contrib.flatpages',

    'newapp.apps.NewappConfig', # назв приложения.apps.из app.ru приложения
    'django_filters',

    #приложения из пакета allauth (три обязательных приложения для работы allauth и одно,
    # которое добавит поддержку входа с помощью Yandex).
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',

    'django_apscheduler', # пакет использует указание времени периодического выполнения задач в стиле сron
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',

                # `allauth` обязательно нужен этот контекстный процессор
                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_REDIRECT_URL = "/news"
# нам нужно «включить» аутентификацию как по #username, так и специфичную по email или сервис-провайдеру
#Далее нам необходимо добавить бэкенды аутентификации:
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', #встроенный бэкенд Django
    'allauth.account.auth_backends.AuthenticationBackend', #бэкенд аутентификации, предоставленный пакетом allauth
]

ACCOUNT_EMAIL_REQUIRED = True #поле email является обязательным
ACCOUNT_UNIQUE_EMAIL = True  #поле email является уникальным.
ACCOUNT_USERNAME_REQUIRED = False #username необязательный
ACCOUNT_AUTHENTICATION_METHOD = 'email'  #аутентификация будет происходить посредством электронной почты.
ACCOUNT_EMAIL_VERIFICATION = 'none'#верификация почты отсутствует


ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'#печать писем в консоль
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #отправка писем на адрес
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "olgalo-a@yandex.ru"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "olgalo-a@yandex.ru" #будет использоваться как значение по умолчанию для поля from в письме.

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"#формат,в кот будет передаваться при рассылке
APSCHEDULER_RUN_NOW_TIMEOUT = 25 #кол-во секунд, за кот функция д вып-ся

SITE_URL ='http://127.0.0.1:8000'

CELERY_BROKER_URL = 'redis://localhost:6379' #указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
CELERY_RESULT_BACKEND = 'redis://localhost:6379' #указывает на хранилище результатов выполнения задач.

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'