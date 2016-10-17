# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0015_transaction_is_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='money',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
