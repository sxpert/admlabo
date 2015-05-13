# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0055_userflag'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='flags',
            field=models.ManyToManyField(to='admtooCore.UserFlag', blank=True),
            preserve_default=True,
        ),
    ]
