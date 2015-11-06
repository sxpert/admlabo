# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0016_userappspecname'),
    ]

    operations = [
        migrations.AddField(
            model_name='userappspecname',
            name='command',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
