# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0015_networkif'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='owner',
            field=models.ForeignKey(blank=True, to='admtooCore.User', null=True),
            preserve_default=True,
        ),
    ]
