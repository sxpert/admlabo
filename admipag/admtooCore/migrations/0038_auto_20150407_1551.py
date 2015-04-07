# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0037_remove_user_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uidnumber',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=True,
        ),
    ]
