# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0013_transaction_is_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='userid',
            name='name',
            field=models.CharField(default='z', max_length=10),
            preserve_default=True,
        ),
    ]
