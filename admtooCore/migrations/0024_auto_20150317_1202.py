# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0023_command'),
    ]

    operations = [
        migrations.RenameField(
            model_name='command',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.AddField(
            model_name='command',
            name='modified',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
