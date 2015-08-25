# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0060_auto_20150805_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailalias',
            name='description',
            field=models.CharField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mailalias',
            name='mail',
            field=models.EmailField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
    ]
