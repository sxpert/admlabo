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
import json
from admtooCore import models
import admtooLib.AdminFunctions as af

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
		if not self._connect() :
			return False
		u = models.User.objects.get (login = user_login)

		# cleanup user data
		email = u.mail if u.mail is not None else ''
		telephone = u.telephone if u.telephone is not None else ''
		poste = telephone[-5:]
		bureau = u.room if u.room is not None else ''
		statut = u.userclass.ref if u.userclass is not None else ''
		equipes = sorted([x.name for x in u.all_teams()])	
		if u.main_team is not None:
			n = u.main_team.name
			# the main team may not be in the list ? what gives
			try :
				idx = equipes.index(n)
			except ValueError as e :
				self._log (u'main team \''+unicode(n)+'\' can\'t be found in list of teams '+unicode(equipes))
			else :
				del equipes[idx]
			equipes.insert(0, n)
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

		if u.display_in_directory() :
			if user is None :
				# can't find user
				self._log ('Annuaire: adding user '+user_login);
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
					self._log ('Annuaire: modifying user : '+user_login)
					keys = sorted(changes.keys())
					values = [changes[k] for k in keys]
					values.append(user_login)
					sql = 'update '+ANNUAIRE_DB_TABLE+' set '+','.join([k+'=%s' for k in keys])+' where id=%s;'
					cursor.execute (sql, values)
				# no changes required
		else :
			if user is not None :
				self._log ('Annuaire: deleting user : '+user_login)
				sql = 'delete from '+ANNUAIRE_DB_TABLE+' where id=%s;'
				cursor.execute (sql, [user_login])

		return True

	def _photo_local_path (self, user) :
		photo_path = user.photo_path if user.photo_path is not None else user.login+'.jpg'
		return os.path.join (settings.USER_PHOTO_PATH,str(user.uidnumber),photo_path)

	def _update_photo (self, user_login) :
		import os.path
		u = models.User.objects.get (login = user_login)
		if u.photo_path is None or len(u.photo_path) == 0:
			self._log (u"FATAL: no file name given for photo")
			return False
		spath = os.path.join (settings.USER_PHOTO_PATH,str(u.uidnumber),u.photo_path)
		self._log (spath)
		dpathl = os.path.join (PHOTO_PATH_LARGE, u.login+'.jpg')
		dpaths = os.path.join (PHOTO_PATH_SMALL, u.login+'.jpg')
		self._log (dpathl)
		self._log (dpaths)
		# copy the original file
		a = af.rem()
		res = a.copy (PHOTO_SERVER, PHOTO_FILE_OWNER, PHOTO_FILE_GROUP, spath, dpathl, PHOTO_FILE_MODE)
		if not res :
			a.log (u'FATAL: unable to copy file '+unicode(spath)+u' to '+unicode(PHOTO_SERVER)+u':'+unicode(dpathl))
			return False
		# resize the picture in a temp file
		import tempfile
		from PIL import Image
		try :
			img = Image.open (spath)
		except IOError as e :
			if e.errno == 21 :
				a.log (u"FATAL: the file corresponds to a directory, no picture")
				return False
		hpercent = (float(MINI_PHOTO_HEIGHT) / float (img.size[1]))
		wsize = int((float(img.size[0]) * float(hpercent)))
		img = img.resize ((wsize, MINI_PHOTO_HEIGHT), Image.ANTIALIAS)
		f = tempfile.NamedTemporaryFile ()
		spath_mini = f.name
		img.save(f, MINI_PHOTO_FORMAT, quality=MINI_PHOTO_QUALITY, optimize=True, progressive=True)
		f.flush()
		# copy the temp file
		res = a.copy (PHOTO_SERVER, PHOTO_FILE_OWNER, PHOTO_FILE_GROUP, spath_mini, dpaths, PHOTO_FILE_MODE)
		f.close()
		if not res :
			a.log (u'FATAL: unable to copy minifile '+unicode(spath_mini)+u' to '+unicode(PHOTO_SERVER)+u':'+unicode(dpaths))
			return False
		return True

	def _fetch_photo (self, user) :
		if user.photo_path is not None :
			self._log (u'SKIPPING '+unicode(user.login)+u' : already have a picture for user')
			return True
		self._log (u'obtaining photo for user '+unicode(user.login))
		spath = os.path.join (PHOTO_PATH_LARGE, user.login+'.jpg')
		dpath = self._photo_local_path (user) 
		self._log (spath)
		a = af.rem()
		fqdn = PHOTO_SERVER
		hostname = a.getHostname(fqdn)
		tpath = os.path.join (os.sep, 'tmp', hostname, spath[1:])
		self._log (u'temporary_path '+unicode(tpath))
		# grab file from server
		res = a.fetch (fqdn, spath, os.path.join (os.sep, 'tmp'))
		if not res :
			a.log (u'FATAL: unable to fetch photo '+unicode(spath)+u' from server to copy it to '+unicode(tpath))
			return False
		# do stuff with file
		self._log (u'moving file to '+unicode(dpath))
		import shutil
		import pwd, grp
		# create destination directory
		try :
			os.makedirs (os.path.dirname(dpath))
		except OSError as e :
			pass
		# move the file
		shutil.move (tpath, dpath)
		# remove the temp file
		shutil.rmtree (os.path.join (os.sep, 'tmp', hostname))
		# change owner of destination file
		uid = pwd.getpwnam(LOCAL_PHOTO_OWNER)[2]
		gid = grp.getgrnam(LOCAL_PHOTO_GROUP)[2]
		os.chown(dpath, uid, gid)
		# change mode of destination file
		os.chmod(dpath, int(PHOTO_FILE_MODE,8))
		# add file to user
		user.photo_path = os.path.basename(dpath)
		user._save()
		return True

	def _init_logger (self, **kwargs) :
		if 'logger' in kwargs.keys() :
			logger = kwargs['logger']
			if logger is not None :
				self._logger = logger

	"""
	mise a jour d'un utilisateur particulier
	"""
	def UpdateUser (self, *args, **kwargs) :
		_, command = args
		self._init_logger(**kwargs)
		c = json.loads(command.data)
		if 'uid' in c.keys() :
			uid = c['uid']
			self._log ('Annuaire.UpdateUser (\''+uid+'\')')
			return self._update_user(uid)
		return False
	
	"""
	mise a jour complete de tout l'annuaire
	"""
	def AnnuaireUpdate (self, *args, **kwargs) :
		self._init_logger(**kwargs)
		users = []
		for u in models.User.objects.all () :
			users.append (u.login)
			if not self._update_user (u.login) :
				return False
		return True 

	"""
	mise a jour de la photo d'un utilisateur
	"""
	def UpdatePhoto (self, *args, **kwargs) :
		_, command = args
		self._init_logger(**kwargs)
		c = json.loads (command.data)
		if 'uid' in c.keys () :
			uid = c['uid']
			self._log ('Annuaire.UpdatePhoto (\''+uid+'\')')
			return self._update_photo (uid)
		return False

			
