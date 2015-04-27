# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect

import logging
logger=logging.getLogger('django')

#==============================================================================
# application dashboard
#
def MainIndex (request) :
	return render(request, 'mainindex.html')
