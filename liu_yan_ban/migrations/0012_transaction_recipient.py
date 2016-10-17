# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0011_auto_20151113_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='recipient',
            field=models.CharField(max_length=100, default=''),
            preserve_default=True,
        ),
    ]
