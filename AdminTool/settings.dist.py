"""
Django settings for admipag project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#	'debug_toolbar',
	'AdminTool',
	'admtooCore',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'AdminTool.urls'

WSGI_APPLICATION = 'AdminTool.wsgi.application'

# Authentication 
AUTHENTICATION_BACKENDS = (
	'django_auth_ldap.backend.LDAPBackend',
#	'django.contrib.auth.backends.ModelBackend',
)


from admtooLib.ldapconfig import osug
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType
AUTH_LDAP_SERVER_URI = osug.OSUG_LDAP_URI

AUTH_LDAP_BIND_DN = osug.OSUG_LDAP_ROOT
AUTH_LDAP_BIND_PASSWORD = osug.OSUG_LDAP_PASS
#AUTH_LDAP_BIND_DN = ""
#AUTH_LDAP_BIND_PASSWORD = ""

AUTH_LDAP_USER_SEARCH = LDAPSearch(osug.OSUG_LDAP_IPAG_PEOPLE_OU+','+osug.OSUG_LDAP_IPAG_BASE,
								   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(osug.OSUG_LDAP_IPAG_GROUP_OU+','+osug.OSUG_LDAP_IPAG_BASE,
									ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)")
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr='cn')
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
	"is_active" : osug.OSUG_LDAP_IPAG_SERVICES_GROUP,
	"is_staff" : osug.OSUG_LDAP_IPAG_SERVICES_GROUP,
	"is_superuser": osug.OSUG_LDAP_IPAG_SERVICES_GROUP
}
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AITH_LDAP_FIND_GROUP_PERMS = True

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#==================================================================================================
#
# Application specific configuration
#

LOGIN_URL          = 'login-form'
DEFAULT_COUNTRY    = 'FR'
DEFAULT_USER_GROUP = 'ipag-pos-site'
ADMIN_DATA_DIR     = 'admtooLibData'
ADMIN_FILES_DIR    = os.path.join(BASE_DIR, ADMIN_DATA_DIR, 'files')
BACKUPPC_SERVER    = 'midgard'
BACKUPPC_USER      = 'backuppc'
BACKUPPC_GROUP     = 'services' 

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     '',
		'USER':		'',
		'PASSWORD': '',
		'HOST':		'localhost',
		'PORT':		'5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_URL = '/static/'
