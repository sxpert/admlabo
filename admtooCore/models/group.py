# -*- coding: utf-8 -*-

import logging
import json
import netfields
from django.db import models, transaction
from django.db.models import Max
from django.conf import settings

LOGGER = logging.getLogger('django')

class Group(models.Model):
    NORMAL_GROUP = 0
    TEAM_GROUP = 1
    SERVICE_GROUP = 2
    STATUS_GROUP = 3

    GROUP_TYPES_CHOICES = (
        (NORMAL_GROUP, ''),
        (TEAM_GROUP, 'Groupe d\'équipe'),
        (SERVICE_GROUP, 'Groupe de service'),
        (STATUS_GROUP, 'Groupe de statut'),
    )
    GROUP_TYPES_PREFIXES = ['', '[T]', '', '[S]']

    gidnumber = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    group_type = models.IntegerField(choices=GROUP_TYPES_CHOICES, default=NORMAL_GROUP)
    parent = models.ForeignKey('self', null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    appspecname = models.TextField(default='', blank=True)

    class Meta(object):
        app_label = 'admtooCore'
        ordering = ['name']

    def __str__(self):
        return self.name

    #
    # finds an available gidnumber within the permitted range
    def _get_next_available_group_id(self):
        last_group = Group.objects.all().aggregate(Max('gidnumber'))['gidnumber__max']
        LOGGER.error('current max gidnumber '+str(last_group))
        group_id = last_group+1
        LOGGER.error('selected next gidnumber '+str(group_id))
        return group_id

    @transaction.atomic
    def create_new(self):
        # step 1: check for ranges
        try:
            ranges = settings.GIDNUMBER_RANGES
        except AttributeError as e:
            # ranges are not defined, consider any gid number is valid
            LOGGER.error('ranges are not defined, finding new group id')
            group_id = self._get_next_available_group_id()
        else:
            # ranges are defined, find a gidnumber within them
            if not isinstance(ranges, list):
                LOGGER.error(u'ERROR: settings.GIDNUMBER_RANGES should be a list '
                             u'of 2-values arrays')
                # things are wrong...
                return False
            # only look for group ids in ranges when ranges are defined
            if len(ranges) > 0:
                LOGGER.error(ranges)
                group_id = None
                # find appropriate group_id
                for group_range in ranges:
                    groups_in_range = Group.objects.filter(gidnumber__gte=group_range[0],
                                                           gidnumber__lte=group_range[1])
                    last_group = groups_in_range.aggregate(Max('gidnumber'))['gidnumber__max']
                    if last_group is None:
                        # did not find any group in the range
                        group_id = group_range[0]
                        break
                    if last_group == group_range[1]:
                        #print "group_id %d would be outside the range - "\
                        #      "looking for another"%(last_group+1)
                        continue
                    # we found a valid last_group in this range
                    group_id = last_group + 1
                    break
                if group_id is None:
                    # no available group number was found in the range
                    return False
                #print "selected group_id %s"%(str(group_id))
            else:
                LOGGER.error(u'There are no ranges defined in the list')
                group_id = self._get_next_available_group_id()
        self.gidnumber = group_id
        # don't involve the external update mechanisms just yet, as nothing is filled in
        # at this point, only the gidnumber is specified
        # this may fail with an IntegrityError
        from django.db import IntegrityError
        try:
            super(Group, self).save()
        except IntegrityError as error:
            LOGGER.error(error)
            return False
        return True

    #
    # removes a group
    #
    def delete(self, user=None):
        from .user import User
        from .usergrouphistory import UserGroupHistory
        creator = None
        if user is not None:
            creator = User.objects.get(login=user)
        # add UserGroupHistory entries for all members
        data = json.dumps({self.gidnumber: self.name})
        for u in self.members():
            ugh = UserGroupHistory()
            ugh.creator = creator
            ugh.user = u
            ugh.action = ugh.ACTION_DEL
            ugh.data = data
            ugh.save()
        # call super.delete
        super(Group, self).delete()

    def destroy(self, user=None):
        # get members list
        g = self.prepare_group_data()
        if g is not None:
            LOGGER.error("destroying group : "+str(g['members']))

        from .command import Command
        c = Command()
        if user is None:
            c.user = "(Unknown)"
        else:
            c.user = user
        c.verb = 'DestroyGroup'
        c.data = json.dumps(g)
        c.save()
        # remove group from database
        # TODO: keep in history table ?
        self.delete(user)


    #
    # return a group identifier for the group list
    # either the name, if not empty, or the gidnumber
    #
    def identifier(self):
        #logger.error (type(self.name))
        if (self.name is not None) and (type(self.name) in (str, unicode,)) and (len(self.name) > 0):
            return self.name
        return self.gidnumber

    def prepare_group_data(self):
        members = self.member_logins()
        g = {}
        if len(self.name) == 0:
            LOGGER.error(u'group has no name yet, skipping')
            return None
        g['cn'] = self.name
        g['gidNumber'] = self.gidnumber
        g['description'] = self.description
        g['members'] = members
        try:
            g['appSpecName'] = json.loads(self.appspecname)
        except ValueError as e:
            g['appSpecName'] = None
        return g

    # update the group object to the ldap server
    def _update_ldap(self, user=None):
        # get members list
        g = self.prepare_group_data()
        #logger.error ("saving group to ldap, members list : "+str(g['members']))
        if g is None:
            LOGGER.error(u'no group data generated, skipping')
            return
        import command, json
        c = command.Command()
        if user is None:
            c.user = "(Unknown)"
        else:
            c.user = user
        c.verb = 'UpdateGroup'
        c.data = json.dumps(g)
        c.save()

    def save(self, *args, **kwargs):
        user = None
        if 'request_user' in kwargs.keys():
            user = kwargs['request_user']
            del kwargs['request_user']
        super(Group, self).save(*args, **kwargs)
        self._update_ldap(user)

    def members(self):
        from .user import User
        return User.objects.filter(groups__name=self.name)

    def member_logins(self):
        m = []
        for u in self.members():
            user = {}
            user['login'] = u.login
            user['first_name'] = u.first_name
            user['last_name'] = u.last_name
            user['appSpecName'] = u.appspecname
            m.append(user)
        return m

    # sets the list of members for a group
    def set_members(self, members, user=None):
        from .user import User
        from .usergrouphistory import UserGroupHistory
        creator = None
        if user is not None:
            creator = User.objects.get(login=user)
        m = []
        for u in members:
            m.append(int(u))

        changed = False

        # remove members not in list
        for u in User.objects.filter(groups__gidnumber=self.gidnumber):
            if u.uidnumber not in m:
                ok = u.remove_group(self.gidnumber, user)
                changed = changed or ok

        # add new members
        for uidnumber in m:
            try:
                u = User.objects.get(uidnumber=uidnumber)
            except User.DoesNotExist as e:
                LOGGER.error(u'Can\'t find user '+unicode(uidnumber))
                pass
            else:
                ok = u.add_group(self.gidnumber, user)
                changed = (changed or ok)

        LOGGER.error(u'group '+unicode(self)+' has changed : '+unicode(changed))

        if changed:
            self._update_ldap(user)

    #
    # helper functions used by the xml template

    def get_children(self):
        return Group.objects.filter(parent=self)

    def group_type_name(self):
        return self.GROUP_TYPES_CHOICES[self.group_type][1]

    def group_type_prefix(self):
        return self.GROUP_TYPES_PREFIXES[self.group_type]

    def is_team_group(self):
        return self.group_type == self.TEAM_GROUP

    def is_service_group(self):
        return self.group_type == self.SERVICE_GROUP

    def is_status_group(self):
        return self.group_type == self.STATUS_GROUP

    # find the groups wiki_team_name
    def wiki_teamlogo(self):
        try:
            asn = json.loads(self.appspecname)
        except ValueError as e:
            return None
        if 'TWikiTeamLogo' in asn:
            return asn['TWikiTeamLogo']
        return None
