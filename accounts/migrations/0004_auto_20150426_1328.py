# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150426_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='head_link',
            field=models.CharField(default=b'default', max_length=255),
            preserve_default=True,
        ),
    ]
