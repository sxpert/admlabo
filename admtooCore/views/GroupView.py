# -*- coding: utf-8 -*-

import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from decorators import *

from .. import models

logger = logging.getLogger('django_auth_ldap')

#
# details of one particular group
#


@admin_login
def group_view(request, group_id):
    g = models.Group.objects.get(gidnumber=group_id)
    action = request.POST.get('action', '').strip()
    if action == 'delete':
        logger.error('destroying group ' + str(g.gidnumber))
        g.destroy(request.user)
        return redirect('groups')

    context = {
        'group': g,
    }
    return render(request, 'group-view.html', context)

#
# creation of new group.
# finds an empty gidnumber to use, create new group with it
# and then passes to the group_view for editing
#


@admin_login
def group_new(request):
    g = models.Group()
    if g.create_new():
        return redirect('group-view', group_id=g.gidnumber)
    else:
        # show the list again with an error in context
        # can only happen when settings.GIDNUMBER_RANGES is defined
        groups = models.Group.objects.all().order_by('name')
        error = "Il n'y a plus de gidNumber disponibles dans les ranges autorisés:\n<ul>"
        for group_range in settings.GIDNUMBER_RANGES:
            error += "<li>%d - %d</li>\n" % (group_range[0], group_range[1])
        error += "</ul>"
        context = {
            'groups': groups,
            'error': error
        }
        return render(request, 'group-list.html', context)

#------------------------------------------------------------------------------
#
# ajax bits for group edit
#
#


def group_view_name_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'options':
        d = g.name
        if d is None:  # should not happen
            d = ''
        data['value'] = d
    if action == 'value':
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'value' in data.keys():
                value = data['value']
                g.name = value
                g.save(request_user=request.user)
        d = g.name
        if d is None:  # should not happen
            d = ''
        data['value'] = d
    return data


def group_view_gidNumber_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'value' and request.method == 'POST':
        data = json.loads(request.body)
        if 'value' in data.keys():
            new_group_id = data['value']
            try:
                new_group_id = int(new_group_id)
            except ValueError:
                data['errors'] = u"Valeur invalide pour un gidNumber, entier positif attendu"
            else:
                response = g.change_gidNumber(new_group_id, request.user)
                # if response is false, gidnumber could not be changed
                if response is False:
                    data['errors'] = u"Impossible de changer le gidNumber, celui ci existe déjà"
                else:
                    # tell the script to reload the page with a new url so as to refresh everything
                    data['redirect'] = reverse('group-view', kwargs = { 'group_id': str(new_group_id) })
                    # update the g variable with the new group
                    g = models.Group.objects.get(gidnumber=new_group_id)
    d = g.gidnumber
    if d is None:  # should not happen
        d = ''
    data['value'] = d
    return data

#
# TWikiName


def group_view_appspecname_variable_field(request, group_id, action, varname):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'options':
        d = g.appspecname
        twikiname = ''
        if d is not None:
            try:
                jsondata = json.loads(d)
            except ValueError as e:
                jsondata = {}
            if varname in jsondata:
                twikiname = jsondata[varname]
        data['value'] = twikiname
    if action == 'value':
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'value' in data.keys():
                value = data['value']
                d = g.appspecname
                try:
                    jsondata = json.loads(d)
                except ValueError as e:
                    jsondata = {}
                jsondata[varname] = value
                g.appspecname = json.dumps(jsondata)
                g.save(request_user=request.user)
        d = g.appspecname
        twikiname = ''
        if d is not None:
            try:
                jsondata = json.loads(d)
            except ValueError as e:
                jsondata = {}
            if varname in jsondata:
                twikiname = jsondata[varname]
        data['value'] = twikiname
    return data


def group_view_members_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'options':
        mem = []
        for u in g.members():
            mem.append(u.uidnumber)
        data['selected'] = mem
        opt = {}
        for u in models.User.objects.filter(user_state=models.User.NORMAL_USER):
            opt[u.uidnumber] = u.full_name()
        data['options'] = opt
    if action == 'value':
        # TODO: post action
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'values' in data.keys():
                values = data['values']
                g.set_members(values, request.user)
        # get current group members
        members = []
        for u in g.members():
            udata = {}
            udata['url'] = reverse('user-view', args=(u.uidnumber,))
            udata['value'] = u.full_name()
            members.append(udata)
        data['values'] = members
    return data


def group_view_members_number_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    data['value'] = len(g.members())
    return data


def group_view_type_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'options':
        data['selected'] = g.group_type
        opt = {}
        for c in g.GROUP_TYPES_CHOICES:
            k, v = c
            opt[k] = v
        data['options'] = opt
        data['noblank'] = True
    if action == 'value':
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'value' in data.keys():
                value = data['value']
                g.group_type = int(value)
                g.save(request_user=request.user)
        data['value'] = g.GROUP_TYPES_CHOICES[g.group_type][1]
    return data


def group_view_parent_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'options':
        if g.parent is not None:
            data['selected'] = g.parent.gidnumber
        else:
            data['selected'] = None
        groups = {}
        for g in models.Group.objects.all():
            groups[g.gidnumber] = g.name
        data['options'] = groups
    if action == 'value':
        if request.method == 'POST':
            # change parent
            data = json.loads(request.body)
            if 'value' in data.keys():
                value = data['value']
                if value is not None:
                    p = models.Group.objects.get(gidnumber=int(value))
                else:
                    p = None
                g.parent = p
                g.save(request_user=request.user)
            pass
        if g.parent is not None:
            d = g.parent.name
            u = reverse('group-view', args=(g.parent.gidnumber,))
        else:
            d = ''
            u = None
        data['value'] = d
        data['url'] = u
    return data


def group_view_description_field(request, group_id, action):
    g = models.Group.objects.get(gidnumber=group_id)
    data = {}
    if action == 'options':
        d = g.description
        if d is None:
            d = ''
        data['value'] = d
    if action == 'value':
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'value' in data.keys():
                value = data['value']
                g.description = value
                g.save(request_user=request.user)
        d = g.description
        if d is None:
            d = ''
        data['value'] = d
    return data


@admin_login
@csrf_protect
def group_view_field(request, group_id, action, fieldtype, fieldname):
    data = {}
    if fieldtype == 'multiselect':
        if fieldname == 'members':
            data = group_view_members_field(request, group_id, action)
    if fieldtype == 'display':
        if fieldname == 'members-number':
            data = group_view_members_number_field(request, group_id, action)
    if fieldtype == 'select':
        if fieldname == 'group-type':
            data = group_view_type_field(request, group_id, action)
        if fieldname == 'parent':
            data = group_view_parent_field(request, group_id, action)
    if fieldtype == 'text':
        if fieldname == 'name':
            data = group_view_name_field(request, group_id, action)
        if fieldname == 'gidNumber':
            data = group_view_gidNumber_field(request, group_id, action)
        # only temporary
        if fieldname == 'TWikiName':
            data = group_view_appspecname_variable_field(
                request, group_id, action, 'twiki')
        if fieldname == 'TWikiTeamLogo':
            data = group_view_appspecname_variable_field(
                request, group_id, action, 'TWikiTeamLogo')

        if fieldname == 'description':
            data = group_view_description_field(request, group_id, action)
    jsdata = json.dumps(data)
    return HttpResponse(jsdata, content_type='application/json')
