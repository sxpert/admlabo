# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0041_command_in_cron'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdir',
            name='files',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
