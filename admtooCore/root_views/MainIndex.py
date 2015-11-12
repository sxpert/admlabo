# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

import logging
logger=logging.getLogger('django')

#==============================================================================
# application dashboard
#
def MainIndex (request) :
	# redirect to the dashboard
	return redirect ('dashboard') 
	return render(request, 'mainindex.html')
