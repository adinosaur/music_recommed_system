# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mymusic', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendedUser', models.ForeignKey(related_name='attendedUser', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='attendingUser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FavSharedMusic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seen', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SharedMusic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('favour', models.IntegerField(default=0)),
                ('song', models.ForeignKey(to='mymusic.Song')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SharedMusicComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('seen', models.BooleanField(default=False)),
                ('sharedMusic', models.ForeignKey(to='social_music.SharedMusic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newsType', models.IntegerField()),
                ('newsID', models.IntegerField()),
                ('fromUser', models.ForeignKey(related_name='FromUser', to=settings.AUTH_USER_MODEL)),
                ('toUser', models.ForeignKey(related_name='ToUser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='favsharedmusic',
            name='sharedMusic',
            field=models.ForeignKey(to='social_music.SharedMusic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favsharedmusic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
