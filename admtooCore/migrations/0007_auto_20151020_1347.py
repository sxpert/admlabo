# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0006_usergrouphistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergrouphistory',
            name='creator',
            field=models.ForeignKey(related_name='ugh_creator', blank=True, to='admtooCore.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usergrouphistory',
            name='user',
            field=models.ForeignKey(related_name='ugh_subject', to='admtooCore.User'),
            preserve_default=True,
        ),
    ]
