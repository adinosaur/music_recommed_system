# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mymusic', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favourite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayMusic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(to='mymusic.Song')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
