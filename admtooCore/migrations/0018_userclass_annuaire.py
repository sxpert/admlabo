# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0017_userappspecname_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='userclass',
            name='annuaire',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
