#coding=utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Song
from models import UserSong
from models import Singer
from pages_assistant import Page_Assistant
# Create your views here.

@login_required
def song_lib(request):
	if request.method == 'GET':
		p = request.GET.get('p', 1)

		#将网页分页展示
		page_assistant = Page_Assistant(count=UserSong.objects.filter(user=request.user).count(), page_size=20)
		pre_page = page_assistant.get_pre_page_no(int(p))
		cur_page = int(p)
		nex_page = page_assistant.get_nex_page_no(int(p))
		page_nums = page_assistant.get_pages_list(cur_page)
		b, e = page_assistant.get_objects_by_pageno(cur_page)
		usersongs = UserSong.objects.filter(user=request.user)[b:e]
		songs = [usersong.song for usersong in usersongs]

		return render_to_response(
			'favour.html', 
			RequestContext(request, {	'songs': songs,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page}))

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
def singer(request):
	if request.method == 'GET':
		p = request.GET.get('p', 1)

		#将网页分页展示
		page_assistant = Page_Assistant(count=Song.objects.filter(singer=request.GET['id']).count(), page_size=20)
		pre_page = page_assistant.get_pre_page_no(int(p))
		cur_page = int(p)
		nex_page = page_assistant.get_nex_page_no(int(p))
		page_nums = page_assistant.get_pages_list(cur_page)
		b, e = page_assistant.get_objects_by_pageno(cur_page)
		songs = Song.objects.filter(singer=request.GET['id'])[b:e]

		user = request.user		
		return render_to_response(
			'index.html', 
			RequestContext(request, {	'songs': songs,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page}))

@login_required
def search_singer(request):
	if request.method == 'GET':
		key = request.GET.get('key', '')
		p = request.GET.get('p', 1)

		print key

		count=Singer.objects.filter(name__contains=key).count()
		#将网页分页展示
		page_assistant = Page_Assistant(count=count, page_size=20)
		pre_page = page_assistant.get_pre_page_no(int(p))
		cur_page = int(p)
		nex_page = page_assistant.get_nex_page_no(int(p))
		page_nums = page_assistant.get_pages_list(cur_page)
		b, e = page_assistant.get_objects_by_pageno(cur_page)
		singers = Singer.objects.filter(name__contains=key)[b:e]

		return render_to_response(
			'singers.html', 
			RequestContext(request, {	'singers': singers,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page}))

@login_required
def search_song(request):
	if request.method == 'GET':
		key = request.GET.get('key', '')
		p = request.GET.get('p', 1)

		count = Song.objects.filter(title__contains=key).count()
		#将网页分页展示
		page_assistant = Page_Assistant(count=count, page_size=20)
		pre_page = page_assistant.get_pre_page_no(int(p))
		cur_page = int(p)
		nex_page = page_assistant.get_nex_page_no(int(p))
		page_nums = page_assistant.get_pages_list(cur_page)
		b, e = page_assistant.get_objects_by_pageno(cur_page)
		songs = Song.objects.filter(title__contains=key)[b:e]

		return render_to_response(
			'index.html', 
			RequestContext(request, {	'songs': songs,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page}))