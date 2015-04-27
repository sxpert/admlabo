# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0014_auto_20150115_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkIf',
            fields=[
                ('mac_addr', netfields.fields.MACAddressField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, blank=True)),
                ('ips', models.ManyToManyField(related_name='networkinterfaces', to='admtooCore.IPAddress', blank=True)),
                ('machine', models.ForeignKey(related_name='interfaces', blank=True, to='admtooCore.Machine', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
