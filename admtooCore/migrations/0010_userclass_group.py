# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0009_newuser_os_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='userclass',
            name='group',
            field=models.ForeignKey(blank=True, to='admtooCore.Group', null=True),
            preserve_default=True,
        ),
    ]
