# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=1000)),
                ('author', models.CharField(default=b'\xe5\x8c\xbf\xe5\x90\x8d', max_length=100)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
                ('is_sensored', models.BooleanField(default=False)),
                ('is_top', models.BooleanField(default=False)),
                ('is_handled', models.BooleanField(default=False)),
                ('user_id', models.IntegerField(default=-1)),
                ('is_viewed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('money', models.IntegerField()),
                ('location', models.CharField(max_length=200)),
                ('shown_name', models.CharField(max_length=100)),
                ('liuyan', models.CharField(max_length=1000)),
                ('is_self', models.BooleanField(default=False)),
                ('user_id', models.IntegerField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('recipient', models.CharField(default=b'', max_length=100)),
                ('is_processed', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'z', max_length=10)),
            ],
        ),
    ]
