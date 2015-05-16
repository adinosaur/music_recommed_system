from django.db import models
from django.contrib.auth.models import User
from mymusic.models import Song
# Create your models here.

class SharedMusic(models.Model):

	user = 	models.ForeignKey(User)
	song = models.ForeignKey(Song)
	comment = models.CharField(max_length=255)
	datetime = models.DateTimeField() 

class Attention(models.Model):
	user = models.ForeignKey(User, related_name='attendingUser')
	attendedUser = models.ForeignKey(User, related_name='attendedUser')