# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0057_user_appspecname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='main_team',
            field=models.ForeignKey(related_name='team_member', blank=True, to='admtooCore.Group', null=True),
            preserve_default=True,
        ),
    ]
