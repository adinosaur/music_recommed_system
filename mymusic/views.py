#coding=utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserMessage
from models import Song
from models import UserSong
from models import Singer
from models import SongComment
from models import FavComment

from datetime import datetime

from pages_assistant import Page_Assistant
# Create your views here.
import os
@login_required
def song_lib(request):
	if request.method == 'GET':
		p = request.GET.get('p', 1)

		#歌曲分页
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
		song = Song.objects.get(pk=song_id)
		p = request.GET.get('p', 1)

		count=SongComment.objects.filter(song=song).count()
		#评论分页
		page_assistant = Page_Assistant(count=count, page_size=20)
		pre_page = page_assistant.get_pre_page_no(int(p))
		cur_page = int(p)
		nex_page = page_assistant.get_nex_page_no(int(p))
		page_nums = page_assistant.get_pages_list(cur_page)
		b, e = page_assistant.get_objects_by_pageno(cur_page)
		comments = SongComment.objects.filter(song=song).order_by("-datetime")[b:e]

		head = UserMessage.objects.get(user=request.user).head

		f = open(os.getcwd() + '/media/music/' + song.lrc_link)
		print os.getcwd() + '/media/music/' + song.lrc_link
		songLyric = f.read()
		f.close()

		for c in comments:
			try:
				FavComment.objects.get(user=request.user, songcomment=c)
				c.isFavour = 1
			except FavComment.DoesNotExist:
				c.isFavour = 0
		#print songLyric
		return render_to_response(
			'play.html', 
			RequestContext(request, {	'user': request.user,
										'song': song,
										'head': head,
										'songLyric': songLyric,
										'comments': comments,
										'comments_count': count,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page})) 

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

		#歌曲分页
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
		#歌手分页
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
		#歌曲分页
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

@csrf_exempt
@login_required
def comment(request):
	if request.method == 'POST':
		songcomment = SongComment()
		try:
			song_id = request.POST['song_id']
		except KeyError, e:
			print "[INFO]mymusic.views.comment: wrong song id!"
			print e

		print "[INFO]mymusic.views.comment: song_id=%s" %request.POST['song_id']
		print "[INFO]mymusic.views.comment: comment=%s" %request.POST['comment']
		songcomment.song = Song.objects.get(pk=song_id)
		songcomment.user = request.user
		songcomment.comment = request.POST.get('comment', '')
		songcomment.datetime = datetime.now()
		print "[INFO]mymusic.views.comment: datetime=",
		print songcomment.datetime
		songcomment.favour = 0
		songcomment.save()
		return HttpResponseRedirect('/mymusic/play?id=%s' %song_id)

@login_required
def favour_comment(request):
	if request.method == 'GET':
		try:
			comment_id = request.GET['id']
		except KeyError:
			print "[ERROR]mymusic.views.favour_comment: worng comment id"
		songcomment = SongComment.objects.get(id=comment_id)
		try:
			favcomment = FavComment.objects.get(songcomment_id=comment_id,user=request.user)
			print "[ERROR]mymusic.views.favour_comment: 已经点过赞了, song id: %d" %songcomment.song.id
		except  FavComment.DoesNotExist:
			songcomment.favour+=1
			songcomment.save()
			favcomment = FavComment()
			favcomment.songcomment=songcomment
			favcomment.user=request.user
			favcomment.save()
			print "[INFO]mymusic.views.favour_comment: 成功点赞, song id: %d" %songcomment.song.id
		else:
			pass
		return HttpResponseRedirect('/mymusic/play?id=%s' %songcomment.song.id)

@login_required
def cancel_favour_comment(request):
	if request.method == 'GET':
		try:
			comment_id = request.GET['id']
		except KeyError:
			print "[ERROR]mymusic.views.cancel_favour_comment: worng comment id"
		print "comment_id: " + comment_id
		songcomment = SongComment.objects.get(id=comment_id)
		songcomment.favour -= 1
		songcomment.save()
		favcomment = FavComment.objects.get(user=request.user, songcomment=songcomment)
		favcomment.delete()
		print "[INFO]mymusic.views.cancel_favour_comment: 成功取消赞, song id: %d" %songcomment.song.id
		return HttpResponseRedirect('/mymusic/play?id=%s' %songcomment.song.id)