# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0002_comment_is_sensored'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_handled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
