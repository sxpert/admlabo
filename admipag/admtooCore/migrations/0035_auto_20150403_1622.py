# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0034_auto_20150401_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='user',
            field=models.ForeignKey(related_name='User', blank=True, to='admtooCore.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='new',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newuser',
            name='manager',
            field=models.ForeignKey(related_name='Manager', blank=True, to='admtooCore.User', null=True),
            preserve_default=True,
        ),
    ]
