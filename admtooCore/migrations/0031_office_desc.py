# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0030_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='desc',
            field=models.CharField(max_length=16, null=True, blank=True),
            preserve_default=True,
        ),
    ]
