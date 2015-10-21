# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0007_auto_20151020_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergrouphistory',
            options={'ordering': ['-created'], 'get_latest_by': 'created'},
        ),
        migrations.AlterField(
            model_name='newuser',
            name='other_office',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
    ]
