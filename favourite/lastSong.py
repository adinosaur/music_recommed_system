#encoding=utf8
from models import PlayMusic
from django.contrib.auth.models import User

def getLastPlayedSong(user):
	return (PlayMusic.objects.filter(user=user).order_by('-datetime')[0]).song

