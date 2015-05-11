# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0049_user_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='appspecname',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
