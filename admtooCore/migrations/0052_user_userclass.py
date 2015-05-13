# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import admtooCore.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0051_mailinglist_userclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userclass',
            field=models.ForeignKey(default=admtooCore.models.user.userclass_default, to='admtooCore.UserClass'),
            preserve_default=True,
        ),
    ]
