from workout_log.settings.base_settings import *

TEMPLATE_DEBUG = DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': abspath(join(PROJECT_ROOT, '..', 'db.sqlite3')),
    }
}

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False
