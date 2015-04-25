from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Song
from models import UserSong
# Create your views here.

@login_required
def song_lib(request):
	usersongs = UserSong.objects.filter(user=request.user)
	songs = [usersong.song for usersong in usersongs]
	return render_to_response('favour.html', RequestContext(request, {'songs': songs,
																	  'user': request.user}))

@login_required
def play(request):
	if request.method == 'GET':
		song_id = request.GET['id']
		_song = Song.objects.get(pk=song_id)
		print _song.pic_link
		return render_to_response('play.html', RequestContext(request, {'song':_song})) 

@login_required
def create_fav(request):
	if request.method == 'GET':

		song = Song.objects.get(pk=request.GET['id'])

		try:
			usersong = UserSong.objects.get(user=request.user, song=song)
		except UserSong.DoesNotExist:
			usersong = UserSong()
			usersong.user = request.user
			usersong.song = Song.objects.get(pk=request.GET['id'])
			usersong.save()
			print "user:%s favour %s" %(usersong.user, usersong.song)
		else:
			pass
		return HttpResponse('create_fav')

@login_required
def remove_fav(request):
	if request.method == 'GET':
		user = request.user
		song = Song.objects.get(pk=request.GET['id'])
		usersong = UserSong.objects.get(user=user, song=song)
		usersong.delete()
		return HttpResponseRedirect('/mymusic/song-lib/')

@login_required
def search_singer(request):
	if request.method == 'GET':
		user = request.user
		songs = Song.objects.filter(singer=request.GET['id'])
		return render_to_response('index.html', RequestContext(request, {'songs': songs,
																	  	  'user': request.user}))