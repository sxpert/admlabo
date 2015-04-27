# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0009_group_group_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='admtooCore.Group', blank=True),
            preserve_default=True,
        ),
    ]
