# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0005_comment_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_viewd',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
