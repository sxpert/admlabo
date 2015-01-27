# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('silabo', '0013_domainname_machine_machineclass_vlan'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('address', netfields.fields.InetAddressField(max_length=39, serialize=False, primary_key=True)),
                ('ptr', models.ForeignKey(blank=True, to='silabo.DomainName', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='domainname',
            name='ips',
            field=models.ManyToManyField(related_name='domainnames', to='silabo.IPAddress', blank=True),
            preserve_default=True,
        ),
    ]
