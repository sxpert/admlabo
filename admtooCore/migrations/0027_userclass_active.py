# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0026_auto_20151202_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='userclass',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
