# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0016_transaction_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default=b'\xe5\x8c\xbf\xe5\x90\x8d', max_length=100),
        ),
    ]
