# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0008_group_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_type',
            field=models.IntegerField(default=0, choices=[(0, b''), (1, b"Groupe d'\xc3\xa9quipe"), (2, b'Groupe de service')]),
            preserve_default=True,
        ),
    ]
