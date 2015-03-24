# -*- coding: utf-8 -*-

from django.shortcuts import render
from .. import models
from django.contrib.auth.decorators import login_required

#
# form that is displayed when a person is to be 
# declared
#

@login_required
def NewArrivalForm (request) :
	return render(request, 'newarrivalform.html')

