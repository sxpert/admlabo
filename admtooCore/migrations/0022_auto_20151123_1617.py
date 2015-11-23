# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0021_newuser_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.utcnow, auto_now_add=True),
            preserve_default=True,
        ),
    ]
