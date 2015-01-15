from workout_log.settings.base_settings import *

TEMPLATE_DEBUG = DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'workout_logger',
        'USER': 'workout_user',
        'PASSWORD': 'password1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False
