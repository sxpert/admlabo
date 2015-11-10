#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# plugin annuaire
#
# serveur					"ipag"
# database					"annuaire_ipag"
# injecte dans la table 	"annuaire"
# 
# NOTE: the mysql setup is too stupid to handle transactions properly
#

"""
| nom       | text        | NO   |     | NULL    |       | 		nom
| prenom    | text        | NO   |     | NULL    |       | 		prénom
| id        | varchar(32) | NO   | PRI | NULL    |       | 		login
| email     | text        | NO   |     | NULL    |       | 		email
| poste     | text        | NO   |     | NULL    |       | 		tel interne
| telephone | text        | NO   |     | NULL    |       | 		SDA
| bureau    | text        | NO   |     | NULL    |       | 		numéro de bureau
| statut    | text        | NO   |     | NULL    |       | 		user class
| equipe1   | text        | NO   |     | NULL    |       | 			// interstellaire
| equipe2   | text        | NO   |     | NULL    |       | 			// cristal
| equipe3   | text        | NO   |     | NULL    |       | 			// admin
| equipe4   | text        | NO   |     | NULL    |       | 			// ingetech
| equipe5   | text        | NO   |     | NULL    |       | 			// planeto
| equipe6   | text        | NO   |     | NULL    |       | 			// sherpas
| equipe7   | text        | NO   |     | NULL    |       | 			// odyssey
| equipe8   | text        | NO   |     | NULL    |       | 			// exoplanetes
| equipe9   | text        | NO   |     | NULL    |       | 			// ?
| tags      | text        | NO   |     | NULL    |       | 		flag_photo_web
| champ2    | text        | NO   |     | NULL    |       | 							// inutile
| champ3    | text        | NO   |     | NULL    |       | 							// inutile
| champ4    | text        | NO   |     | NULL    |       | 							// inutile
"""


import logging
from django.conf import settings
from config.annuaire import *
import MySQLdb
import types
from admtooCore import models

class Annuaire (object) :
	def __init__ (self) :
		self._logger = None

	def _log (self, message) :
		if self._logger is None :
			logging.basicConfig (level=logging.INFO)
		if self._logger is not None :
			self._logger.error (message)
		else:
			logging.info (message)

	def _connect (self) :
		try :
			self._db = MySQLdb.connect (host=ANNUAIRE_DB_SERVER, db=ANNUAIRE_DB_NAME, user=ANNUAIRE_DB_USER, passwd=ANNUAIRE_DB_PASS)
		except MySQLdb.Error as e :
			if e[0] == 1130 :
				self._log(u'FATAL : can\'t connect to server : '+unicode(e[1]))
				return False
		self._db.autocommit(False)
		return True

	def _read_one (self, cursor) :
		row = cursor.fetchone()
		if row is None :
			return None
		fields = map(lambda x: x[0], cursor.description)
		result = dict(zip(fields, row))
		return result

	def _disconnect (self) :
		self._db.close()
		pass

	def _update_user (self, user_login) :
		self._connect()
		u = models.User.objects.get (login = user_login)

		# cleanup user data
		email = u.mail if u.mail is not None else ''
		telephone = u.telephone if u.telephone is not None else ''
		poste = telephone[-5:]
		bureau = u.room if u.room is not None else ''
		statut = (u.userclass.fr if u.userclass.fr is not None else u.userclass.ref) if u.userclass is not None else ''
		equipes = sorted([x.name for x in u.all_teams()])	
		if u.main_team is not None:
			del equipes[equipes.index(u.main_team.name)]
			equipes.insert(0, u.main_team.name)
		tags = [x.name for x in u.flags.all() if x.name==settings.FLAG_PHOTO_WEB]
		tags = tags[0] if len(tags)>0 else ''

		# generate user dictionnary
		new = {}

		new['nom']       = u.last_name.encode('utf-8')
		new['prenom']    = u.first_name.encode('utf-8')
		new['id']        = u.login
		new['email']     = email
		new['poste']     = poste
		new['telephone'] = telephone	
		new['bureau']    = bureau
		new['statut']    = statut.encode('utf-8')
		for i in range(0,9) :
			new['equipe'+str(i+1)] = equipes[i] if i<len(equipes) else ''
		new['tags']      = tags
		for i in range(2,5) :
			new['champ'+str(i)] = ''

		# various things depending on status		

		sql = 'select * from '+ANNUAIRE_DB_TABLE+' where id=%s;'
		cursor = self._db.cursor()
		try :
			cursor.execute (sql, (user_login,))
		except Exception as e :
			self._log (e)
			self._db.rollback ()
			return False
		user = self._read_one(cursor)
		fields = [x[0] for x in cursor.description]

		if u.user_state == u.NORMAL_USER :
			if user is None :
				# can't find user
				self._log (u'adding user '+user_login);
				# insert new user
				sql = 'insert into '+ANNUAIRE_DB_TABLE+' ('
				sql+= ','.join(fields)
				sql+= ') values ('
				sql+= ','.join(['%s' for i in range(0,21)])
				sql+= ');'
				values = [new[i] for i in fields]
				cursor.execute (sql, values)
			else :
				# calculate changes
				changes = dict((key, new[key]) for key in fields if (new[key]!=user[key]))
				if len(changes)>0 :
					self._log ('modifying user : '+user_login)
					keys = sorted(changes.keys())
					values = [changes[k] for k in keys]
					values.append(user_login)
					sql = 'update '+ANNUAIRE_DB_TABLE+' set '+','.join([k+'=%s' for k in keys])+' where id=%s;'
					cursor.execute (sql, values)
				# no changes required
		else :
			if user is not None :
				self._log ('deleting user : '+user_login)
				sql = 'delete from '+ANNUAIRE_DB_TABLE+' where id=%s;'
				cursor.execute (sql, [user_login])

		return True
	
	"""
	mise a jour complete de tout l'annuaire
	"""
	def AnnuaireUpdate (self, *args, **kwargs) :
		self._connect ()
		users = []
		for u in models.User.objects.all () :
			users.append (u.login)
			if not self._update_user (u.login) :
				return False
		return True 

