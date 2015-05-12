# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0050_group_appspecname'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='userclass',
            field=models.ForeignKey(blank=True, to='admtooCore.UserClass', null=True),
            preserve_default=True,
        ),
    ]
