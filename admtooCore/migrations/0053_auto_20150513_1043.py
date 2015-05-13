# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import admtooCore.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0052_user_userclass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userclass',
            field=models.ForeignKey(default=admtooCore.models.user.userclass_default, blank=True, to='admtooCore.UserClass', null=True),
            preserve_default=True,
        ),
    ]
