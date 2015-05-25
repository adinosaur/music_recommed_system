# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('social_music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernews',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 25, 10, 10, 26, 544386), auto_now=True),
            preserve_default=False,
        ),
    ]
