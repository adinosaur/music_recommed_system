#encoding=utf8
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from algorithm import update_favourite
from algorithm import get_similar_song
from algorithm import get_similar_userlove
from algorithm import get_random_song

from models import PlayMusic

@login_required
def played(request):
	if request.method == "GET" and 'songid' in request.GET:
		userid = request.user.pk
		songid = request.GET['songid']
		behave = 'full_listen'
		update_favourite(userid, songid, behave)

@login_required
def collected(request):
	if request.method == "GET" and 'songid' in request.GET:
		userid = request.user.pk
		songid = request.GET['songid']
		behave = 'collected'
		update_favourite(userid, songid, behave)

@login_required
def shared(request):
	if request.method == "GET" and 'songid' in request.GET:
		userid = request.user.pk
		songid = request.GET['songid']
		behave = 'shared'
		update_favourite(userid, songid, behave)

@login_required
def recommendByUser(request):
	userid = request.user.pk
	n = 5
	sidlist = json.dumps(get_similar_userlove(userid, n))
	return HttpResponse(sidlist, content_type='application/json')
	
@login_required
def recommendBySong(request):
	if request.GET['sid']:
		songid = request.GET['sid']
		n = 5
		sidlist = json.dumps(get_similar_song(songid, n))
		return HttpResponse(sidlist, content_type='application/json')
	
@login_required
def recommendByRandom(request):
	n = 5
	sidlist = json.dumps(get_random_song(n))
	return HttpResponse(sidlist, content_type='application/json')
	
@login_required
def markdownPlayEvent(request):
	if request.method == 'GET' and 'song_id' in request.GET:
		userid = request.user.pk
		songid = int(request.GET['song_id'])
		playmusic = PlayMusic(user_id = userid, song_id = songid)
		playmusic.save()
		
		behave = 'full_listen'
		update_favourite(userid, songid, behave)
