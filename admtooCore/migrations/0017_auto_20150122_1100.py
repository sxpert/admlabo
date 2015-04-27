# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0016_machine_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['login']},
        ),
        migrations.AddField(
            model_name='machine',
            name='comment',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='networkif',
            name='addressing_type',
            field=models.IntegerField(default=2, choices=[(0, b'statique'), (1, b'dhcp statique'), (2, b'dhcp')]),
            preserve_default=True,
        ),
    ]
