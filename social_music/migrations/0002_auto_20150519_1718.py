# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('fuser', models.ForeignKey(related_name='replyingUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SharedMusicComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('favour', models.IntegerField(default=0)),
                ('sharedMusic', models.ForeignKey(to='social_music.SharedMusic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reply',
            name='sharedmusiccomment',
            field=models.ForeignKey(to='social_music.SharedMusicComment'),
        ),
        migrations.AddField(
            model_name='reply',
            name='tuser',
            field=models.ForeignKey(related_name='replyedUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
