# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_music', '0002_sharedmusiccomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharedmusiccomment',
            name='favour',
        ),
        migrations.AddField(
            model_name='sharedmusic',
            name='favour',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
