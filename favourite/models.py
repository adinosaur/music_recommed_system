from django.db import models
from django.contrib.auth.models import User
from mymusic.models import Song

# Create your models here.
class Favourite(models.Model):
	user = models.ForeignKey(User)
	song = models.ForeignKey(Song)
	love = models.IntegerField()

	class Meta:
		unique_together = ('user', 'song')
	primary = ('user', 'song')

	def __unicode__(self):
		return user.id + "," + song.id
		
class PlayMusic(models.Model):
	user = models.ForeignKey(User)
	song = models.ForeignKey(Song)
	datetime = models.DateTimeField(auto_now_add=True)
