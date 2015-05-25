# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_music', '0003_auto_20150525_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernews',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
