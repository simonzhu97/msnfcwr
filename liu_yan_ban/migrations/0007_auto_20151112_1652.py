# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liu_yan_ban', '0006_comment_is_viewd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='is_viewd',
            new_name='is_viewed',
        ),
    ]
