# Django settings for emancala project.

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

import sys
sys.path.append(os.path.join(PROJECT_PATH, '..', '..',))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SEND_BROKEN_LINK_EMAILS = True
EMAIL_SUBJECT_PREFIX = '[Emancala] '

ADMINS = (
    ('Dougal Matthews', 'dougal@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'control_group5'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'Zeppelin1'
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pk4y!_-)&h+uojqd6o_+%_g$t11@1$_s7-zy61r^%p0$w(jsy='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'emancala.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.csrf',
    'django.contrib.databrowse',
    'django.contrib.flatpages',
    'django.contrib.formtools',
    'django.contrib.humanize',
    'django.contrib.localflavor',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.syndication',
    'django.contrib.webdesign',
    
    'pycala.web.emancala',
    
    # just so we can easily access the models via the ORM
    'pycala.players.nn',
)
