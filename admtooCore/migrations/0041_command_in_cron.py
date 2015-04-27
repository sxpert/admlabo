# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0040_user_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='in_cron',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
