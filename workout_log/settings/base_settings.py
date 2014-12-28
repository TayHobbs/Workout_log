from os.path import abspath, join, dirname

PROJECT_ROOT = abspath(join(dirname(__file__), '..'))
ENV = None

TEMPLATE_DEBUG = DEBUG = False
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = False
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_URL = '/static/'
SECRET_KEY = '!9oxr(8k34^z)&l#i-hvb0^i1#6x$zg2)(t4jbjvc99_ma4kor'
STATICFILES_DIRS = (
    abspath(join(PROJECT_ROOT, "..", "static")),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
ROOT_URLCONF = 'workout_log.urls'
WSGI_APPLICATION = 'workout_log.wsgi.application'
TEMPLATE_DIRS = (
    abspath(join(PROJECT_ROOT, 'templates'))
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PROJECT_APPS = (
    'logs',
)

INSTALLED_APPS = (
    'rest_framework',
    'south',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
) + PROJECT_APPS

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
