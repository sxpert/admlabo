# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0007_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
    ]
