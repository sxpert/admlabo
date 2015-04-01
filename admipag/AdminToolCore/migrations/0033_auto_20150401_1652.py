# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import AdminToolCore.models.newuser


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0032_newuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='arrival',
            field=models.DateField(default=AdminToolCore.models.newuser.arrival_default),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='birthdate',
            field=models.DateField(default=AdminToolCore.models.newuser.birthdate_default),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='chem_lab',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='citizenship',
            field=models.ForeignKey(default=AdminToolCore.models.newuser.citizenship_default, to='AdminToolCore.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='comments',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='comp_account',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='comp_purchase',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='departure',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='external_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='first_name',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='ir_lab',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='manager',
            field=models.ForeignKey(blank=True, to='AdminToolCore.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='risky_activity',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='specific_os',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='status',
            field=models.ForeignKey(default=AdminToolCore.models.newuser.status_default, to='AdminToolCore.UserClass'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newuser',
            name='workshop',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
