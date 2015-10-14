# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0002_auto_20150902_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_type',
            field=models.IntegerField(default=0, choices=[(0, b''), (1, b"Groupe d'\xc3\xa9quipe"), (2, b'Groupe de service'), (3, b'Groupe de statut')]),
            preserve_default=True,
        ),
    ]
