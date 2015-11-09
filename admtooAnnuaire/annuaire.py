#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# plugin annuaire
#
# serveur					"ipag"
# database					"annuaire_ipag"
# injecte dans la table 	"annuaire"
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
		self._log ('-----------------------------------------------------------------')
		self._connect()
		u = models.User.objects.get (login = user_login)
		sql = 'select * from '+ANNUAIRE_DB_TABLE+' where id=%s for update;'
		cursor = self._db.cursor()
		try :
			cursor.execute (sql, (user_login,))
		except Exception as e :
			self._log (e)
			self._db.rollback ()
			return False
		user = self._read_one(cursor)
		if user is None :
			# can't find user
			self._log (u'unable to find user '+user_login);
			# insert new user
			sql = 'insert into '+ANNUAIRE_DB_TABLE+' ('
			sql+= 'nom,prenom,id,email,poste,telephone,bureau,statut,'
			teams = []
			for i in range(1, 10) :
				teams.append ('equipe'+str(i))
			sql+=','.join (teams)+','
			sql+= ',tags,champ2,champ3,champ4'
			sql+= ') values ('
			values = []
			for i in range(0, 21) :
				values.append('%s')
			sql+= ','.join(values)
			sql+= ');'
			self._log (sql)

			values = []

			values.append (u.last_name)
			values.append (u.first_name)
			values.append (u.login)
			mail = u.mail
			if mail is None :
				mail = ''
			values.append (mail)		
			telephone = u.telephone
			if telephone is None :
				telephone = ''
			values.append (telephone[-5:])
			values.append (telephone)
			room = u.room
			if room is None :
				room = ''
			values.append (room)
			userclass = u.userclass
			if userclass is None :
				userclass = ''
			else :	
				userclass = userclass.ref
			values.append (userclass)
			teams = u.all_teams()
			tm = []
			for t in teams :	
				tm.append (t.name)
			for i in range (1,10) :
				try :
					t = tm[i]
				except IndexError as e:
					t = ''
				values.append (t)
			flags = u.flags.all()
			tf = []
			for f in flags :
				tf.append (f.name)
			if settings.FLAG_PHOTO_WEB in tf :
				values.append (settings.FLAG_PHOTO_WEB)
			else:	
				values.append ('')
			for i in range(1,3) :
				values.append ('')
			self._log (values)

		else :	
			# user is found
			changes = {}
			
			if u.mail != user['email'] :
				changes['email'] = u.mail
			
			telephone = u.telephone
			if telephone is None : 
				telephone = ''
			poste = telephone[-5:]
			if poste != user['poste'] :
				changes['poste'] = poste

			if telephone != user['telephone'] :
				changes['telephone'] = telephone

			room = u.room
			if room is None :
				room = ''
			if room != user['bureau'] :
				changes['bureau'] = room

			userclass = u.userclass
			if userclass is None :
				self._log (u'FATAL: user '+unicode(user_login)+u' has no userclass')
				return False
			if userclass.ref != user['statut'] :
				changes['statut'] = userclass.ref

			# hanle teams
			teams = u.all_teams()
			tm = []
			for t in teams :
				tm.append(t.name)
			teams = tm
			old_teams = []
			for i in range(1,10) :
				tn = 'equipe'+str(i)
				if (tn in user) and (user[tn] is not None) and (user[tn] != '') :
					old_teams.append (user[tn])
			old_teams.sort()
			# search for teams not in old teams
			new_teams = []
			for t in teams :
				if t not in old_teams :
					new_teams.append (t)
			del_teams = []
			for t in old_teams :
				if t not in teams :
					del_teams.append (t)
			
			# if either new_teams or del_teams not empty, teams have changed...
			if (len(new_teams) > 0) or (len(del_teams)>0) :	
				for i in range (1, 10) :
					try :
						t = teams[i-1]
					except IndexError as e:
						t = ''
					if t is None :
						t = ''
					changes['equipe'+str(i)] = t

			flags = u.flags.all()
			# some debugging needed
			tags = ''
			if len(flags) > 0 :
				fnames = []
				for f in flags :
					fnames.append (f.name)
				if settings.FLAG_PHOTO_WEB in fnames :
					tags = settings.FLAG_PHOTO_WEB
			if tags != user['tags'] : 
				changes['tags'] = tags

			sql = 'update '+ANNUAIRE_DB_TABLE+' set '
			fields = changes.keys()
			fields.sort()
			entries = []
			values = []
			for f in fields :
				entries.append (f+'=%s')
				values.append (changes[f])

			if (len(values) > 0) :
				sql+=', '.join (entries)
				sql+=' where id = %s ;'
				values.append (user_login)
				self._log (sql)
				self._log (values)

				cursor.execute (sql, values)
				#self._db.commit ()

	"""
	mise a jour complete de tout l'annuaire
	"""
	def AnnuaireUpdate (self, *args, **kwargs) :
		self._connect ()
		for u in models.User.objects.filter (user_state=models.User.NORMAL_USER) :
			self._update_user (u.login)

