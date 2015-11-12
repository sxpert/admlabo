# -*- coding: utf-8 -*-

import os, os.path

ANNUAIRE_DB_SERVER = 'ipag'
ANNUAIRE_DB_NAME   = 'annuaire'
ANNUAIRE_DB_USER   = 'user'
ANNUAIRE_DB_PASS   = 'pass'
ANNUAIRE_DB_TABLE  = 'table'

PHOTO_SERVER	   = 'localhost'
PHOTO_FILE_OWNER   = 'apache'
PHOTO_FILE_GROUP   = 'apache'
PHOTO_FILE_MODE    = '0644'

MINI_PHOTO_HEIGHT  = 225
MINI_PHOTO_FORMAT  = 'JPEG'
MINI_PHOTO_QUALITY = 80

PHOTO_PATH_LARGE   = os.path.join (os.sep, 'var', 'www', 'annuaire_ipag', 'trombi-original')
PHOTO_PATH_SMALL   = os.path.join (os.sep, 'var', 'www', 'annuaire_ipag', 'trombi300x225')

		
		
		

