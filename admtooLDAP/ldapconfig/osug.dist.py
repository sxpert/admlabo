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
