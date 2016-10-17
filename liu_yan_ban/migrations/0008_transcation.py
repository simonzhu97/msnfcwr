# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0007_auto_20151112_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('location', models.CharField(max_length=200)),
                ('shown_name', models.CharField(max_length=100)),
                ('liuyan', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
