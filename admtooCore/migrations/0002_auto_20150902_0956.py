# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0001_squashed_0062_remove_mailalias_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo_is_public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='photo_path',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
    ]
