# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silabo', '0020_user_login_shell'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkif',
            name='ips',
            field=models.ManyToManyField(related_name='networkinterfaces', db_index=True, to='silabo.IPAddress', blank=True),
            preserve_default=True,
        ),
    ]
