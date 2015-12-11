# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0027_userclass_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='handled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
