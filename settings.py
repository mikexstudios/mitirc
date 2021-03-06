# Django settings for project.
import os
import django
import sys

# Path of Django framework files (no trailing /):
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
# Path of this "site" (no trailing /):
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #We rigorously set the path to the sqlite3 db since standalone scripts will
        #have the CWD different than when run with manage.py
        'NAME': os.path.join(SITE_ROOT, 'development.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kwj%q_c9k$_ham%hvhp9mf!wxri9e1-k3+7rdmkkck+zc)xbh6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'south', #database migrations
    #'djcelery', #messaging queue
    #'djkombu', #for using orm as ghetto queue

    'cas_consumer', #for SSO signins with MIT certs

    'base',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request', #for request object
    'django.contrib.messages.context_processors.messages',
    #Above are the default template context processors
    #'yourapp.context_processors.sitename',
)

AUTHENTICATION_BACKENDS = (
    #'django_rpx_plus.backends.RpxBackend', 
    'cas_consumer.backends.CASBackend',
    'django.contrib.auth.backends.ModelBackend', #default django auth
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/dashboard/' #default: '/accounts/profile/'

###################
# base app settings
###################

#WEBCHAT_URL = 'http://localhost:9090/'
DEFAULT_ROOM = '#general'
#The room age filter defines the cutoff for if a room is displayed on dashboard
#if it hasn't been updated in t minutes. Default is 10 minutes.
ROOM_AGE_FILTER = 10 #minutes

IRC_SERVER = 'yourserver'
IRC_SERVER_PORT = 6667
IRC_TASK_NICKNAME = 'guest-task'

#How often should the list of IRC rooms be updated in the dashboard? (specify value
#in seconds; default is 1 minute)
IRC_UPDATE_INTERVAL = 60 #sec


##############################
# django-cas-consumer settings
##############################
CAS_BASE = 'http://mxh.scripts.mit.edu/mitauth/'
CAS_COMPLETELY_LOGOUT = False #don't notify CAS provider of logout
CAS_EMAIL_CALLBACK = lambda username: '%s@mit.edu' % username


###################
# djcelery settings 
###################
#import djcelery
#djcelery.setup_loader()
#
##Result store settings.
#CELERY_RESULT_BACKEND = 'database' #default = database
##CELERY_RESULT_DBURI = 'mysql://%s:%s@%s/%s' % ()
#CELERY_RESULT_DBURI = 'sqlite://celerydb.sqlite'
#
#BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
##BROKER_TRANSPORT = 'djkombu.transport.DatabaseTransport'
##BROKER_HOST = 'localhost'
##BROKER_PORT = 5672
##BROKER_USER = 'dev'
##BROKER_PASSWORD = 'testtest'
##BROKER_VHOST = 'mXs-MBP'
#
##If True, tasks are executed locally and never sent to queue.
##CELERY_ALWAYS_EAGER = True
##CELERYD_LOG_LEVEL = 'INFO'
#
##CELERYD_CONCURRENCY = '2' #default = number of CPU
#
##List of modules to import when celery starts.
#CELERY_IMPORTS = ('base.tasks', )



#Import any local settings (ie. production environment) that will override
#these development environment settings.
try:
    from local_settings import *
except ImportError:
    pass 
