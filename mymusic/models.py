from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Singer(models.Model):
	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=255)

class Song(models.Model):
	def __unicode__(self):
		return self.title

	title = models.CharField(max_length=255)
	singer = models.ForeignKey(Singer)
	pic_link = models.CharField(max_length=255)
	song_link = models.CharField(max_length=255)
	lrc_link = models.CharField(max_length=255)	

class UserSong(models.Model):
	def __unicode__(self):
		return self.title

	user = models.ForeignKey(User)
	song = models.ForeignKey(Song)

class SongComment(models.Model):
	def __unicode__(self):
		return self.song

	song = models.ForeignKey(Song)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length=255)
	time = models.DateField()
	favour = models.IntegerField(default=0)




