# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .. import models
from decorators import *

import logging
logger = logging.getLogger('django_auth_ldap')

@admin_login
def machine_view (request, machine_id) :
    m = models.Machine.objects.get(pk = machine_id)
    context = {
        'machine' : m,
    }
    return render(request, 'machine-view.html', context)

