# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0028_auto_20150326_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ipaddress',
            options={'verbose_name_plural': 'IP Addresses'},
        ),
        migrations.AlterModelOptions(
            name='mailinglist',
            options={'ordering': ['ml_id']},
        ),
        migrations.AddField(
            model_name='country',
            name='eu_member',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
