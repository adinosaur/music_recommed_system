from django.db import models
from django.contrib.auth.models import User
from mymusic.models import Song
# Create your models here.

class SharedMusic(models.Model):
	user = 	models.ForeignKey(User)
	song = models.ForeignKey(Song)
	comment = models.CharField(max_length=255)
	datetime = models.DateTimeField() 
	favour = models.IntegerField(default=0) 

class Attention(models.Model):
	user = models.ForeignKey(User, related_name='attendingUser')
	attendedUser = models.ForeignKey(User, related_name='attendedUser')

class SharedMusicComment(models.Model):
	sharedMusic = models.ForeignKey(SharedMusic)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length=255)
	datetime = models.DateTimeField()

class FavSharedMusic(models.Model):
	sharedMusic = models.ForeignKey(SharedMusic)
	user = models.ForeignKey(User)

class UserNews(models.Model):
	fromUser = models.ForeignKey(User, related_name='FromUser')
	toUser = models.ForeignKey(User, related_name='ToUser')
	newsType = models.IntegerField()# 0: SharedMusicComment; 1: FavSharedMusic
	newsID = models.IntegerField()
	datetime = models.DateTimeField(auto_now=True)
	seen = models.BooleanField(default=False)
