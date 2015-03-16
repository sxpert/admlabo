# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0021_auto_20150311_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(unique=True, max_length=64, db_index=True),
            preserve_default=True,
        ),
    ]
