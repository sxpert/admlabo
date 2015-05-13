# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0053_auto_20150513_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userclass',
            field=models.ForeignKey(blank=True, to='admtooCore.UserClass', null=True),
            preserve_default=True,
        ),
    ]
