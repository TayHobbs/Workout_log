from workout_log.settings.base_settings import *

TEMPLATE_DEBUG = DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'workout_logger',
        'USER': 'taylor.hobbs',
        'PASSWORD': 'asdf',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False
