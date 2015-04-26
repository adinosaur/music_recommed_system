# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150426_1328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermessage',
            old_name='head_link',
            new_name='head',
        ),
    ]
