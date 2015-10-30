# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0013_auto_20151027_0948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['login'], 'permissions': (('do_rh_tasks', 'can change photos and flags'),)},
        ),
    ]
