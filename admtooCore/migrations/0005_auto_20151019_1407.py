# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0004_auto_20151016_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='obs_a',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='osug_d',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='phy_d',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
