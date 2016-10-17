# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0012_transaction_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_delivered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
