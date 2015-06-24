#encoding=utf8
from models import PlayMusic
from django.contrib.auth.models import User
from mymusic.models import Song

def getLastPlayedSong(user):
	try:
		print PlayMusic.objects.filter(user=user).order_by('-datetime')
		lastSong = (PlayMusic.objects.filter(user=user).order_by('-datetime')[0]).song
	except (PlayMusic.DoesNotExist, IndexError):
		lastSong = Song.objects.all()[0]
	return lastSong

