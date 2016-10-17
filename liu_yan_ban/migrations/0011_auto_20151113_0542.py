# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0010_transaction_is_confirm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='is_confirm',
            new_name='is_confirmed',
        ),
    ]
