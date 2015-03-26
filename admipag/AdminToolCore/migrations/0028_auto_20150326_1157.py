# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0027_auto_20150326_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userclass',
            options={'ordering': ['ref'], 'verbose_name_plural': 'UserClasses'},
        ),
        migrations.RenameField(
            model_name='userclass',
            old_name='name',
            new_name='ref',
        ),
        migrations.AddField(
            model_name='userclass',
            name='en',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userclass',
            name='fr',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
