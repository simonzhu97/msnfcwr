# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0009_auto_20151113_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_confirm',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
