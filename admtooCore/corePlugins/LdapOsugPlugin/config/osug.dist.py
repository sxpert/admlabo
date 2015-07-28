# -*- coding: utf-8 -*-

DEBUG = True

OSUG_LDAP_CONFIG = {
	False : {
			},
	True :	{
				'URI' :                'ldap://ldap.example.com',
				'BASE' :               'dc=example,dc=com',
				'ROOT' :               'cn=root,dc=example,dc=com',
				'PASS' :               'password',
				'LABS_OU' : {
						'LAB' :        'ou=lab'
					},
				'PEOPLE_OU':           'ou=people',
				'GROUP_OU':            'ou=group',
				'SERVICES_GROUP' : {
						'lab' :        'cn=lab-services'
					}
			}
		}

OSUG_LDAP_URI  = 'ldap://ldap.example.com'
OSUG_LDAP_BASE = 'dc=example,dc=com'
OSUG_LDAP_ROOT = 'cn=root,dc=example,dc=com'
OSUG_LDAP_PASS = 'password'

OSUG_LDAP_IPAG_BASE = 'dc=example,dc=com'
OSUG_LDAP_IPAG_PEOPLE_OU = 'ou=people'
OSUG_LDAP_IPAG_GROUP_OU = 'ou=group'

OSUG_LDAP_IPAG_PERMANENT_GROUP = 'cn=permanent,'+OSUG_LDAP_IPAG_GROUP_OU+','+OSUG_LDAP_IPAG_BASE
OSUG_LDAP_IPAG_SERVICES_GROUP = 'cn=services,'+OSUG_LDAP_IPAG_GROUP_OU+','+OSUG_LDAP_IPAG_BASE
