# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0056_user_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='appspecname',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
