# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0033_auto_20150401_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='office',
            field=models.ForeignKey(blank=True, to='admtooCore.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='other_office',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='study_level',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='team',
            field=models.ForeignKey(blank=True, to='admtooCore.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='ujf_student',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
