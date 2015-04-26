# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150426_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessage',
            name='head_link',
            field=models.CharField(default=b'/media/heads/default', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='intro',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
