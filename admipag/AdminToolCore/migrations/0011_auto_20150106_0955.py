# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0010_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='arrival',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='departure',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
