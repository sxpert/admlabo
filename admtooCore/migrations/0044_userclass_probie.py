# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0043_emailalert'),
    ]

    operations = [
        migrations.AddField(
            model_name='userclass',
            name='probie',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
