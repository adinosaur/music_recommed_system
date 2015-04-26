# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymusic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='song',
            name='singer',
            field=models.ForeignKey(to='mymusic.Singer'),
            preserve_default=True,
        ),
    ]
