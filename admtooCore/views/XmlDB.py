# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from ..models import *

import logging
logger=logging.getLogger('django')

def XmlDB (request) :
	logger.error('generating XML view')
	context = {}
	context['groups'] = Group.objects.filter(parent=None)
	context['users'] = User.objects.all()
	
	return render(request, 'xml-db.xml', context, content_type="text/xml")

