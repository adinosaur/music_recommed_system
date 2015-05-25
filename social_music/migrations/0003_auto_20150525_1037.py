# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_music', '0002_usernews_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favsharedmusic',
            name='seen',
        ),
        migrations.RemoveField(
            model_name='sharedmusiccomment',
            name='seen',
        ),
        migrations.AddField(
            model_name='usernews',
            name='seen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
