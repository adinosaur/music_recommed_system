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
from social_music.models import UserNews
from favourite.algorithm import update_favourite
from datetime import datetime
from pages_assistant import Page_Assistant
from search_prompt import SearchPromptList
from favourite.lastSong import getLastPlayedSong
from favourite.algorithm import get_similar_song
from favourite.algorithm import get_similar_song2
import json
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
		
		#读取新消息的数量
		newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
		
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)
		
		return render_to_response(
			'favour.html', 
			RequestContext(request, {	'last_song': last_song,
										'songs': songs,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page,
										'newsCount': newsCount}))

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

		#读取新消息的数量
		newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
		
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)
		
		#相似的歌曲
		similarSongsList = get_similar_song2(song_id, 5)
		print similarSongsList
		
		return render_to_response(
			'play.html', 
			RequestContext(request, {	'last_song': last_song,
										'user': request.user,
										'song': song,
										'head': head,
										'songLyric': songLyric,
										'comments': comments,
										'comments_count': count,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page,
										'newsCount': newsCount,
										'similarSongsList': similarSongsList})) 

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
			
			#favourite模块
			behave = 'collected'
			update_favourite(usersong.user.pk, usersong.song.pk, behave)
			print "[INFO]create_fav: user_id:%s, song_id:%s, %s" %(usersong.user.pk, usersong.song.pk, behave)
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
		#读取新消息的数量
		newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
		
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)
		
		return render_to_response(
			'index.html', 
			RequestContext(request, {	'last_song': last_song,
										'songs': songs,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page,
										'newsCount': newsCount}))

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

		#读取新消息的数量
		newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
		
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)
		
		return render_to_response(
			'singers.html', 
			RequestContext(request, {	'last_song': last_song,
										'singers': singers,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page,
										'newsCount': newsCount}))

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

		#读取新消息的数量
		newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
		
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)
		
		return render_to_response(
			'index.html', 
			RequestContext(request, {	'last_song': last_song,
										'songs': songs,
										'user': request.user,
										'page_nums': page_nums,
										'pre_page': pre_page,
										'cur_page': cur_page,
										'nex_page': nex_page,
										'newsCount': newsCount}))

@login_required
def search_prompt(request):
	if request.method == 'GET':
		searchPromptList = SearchPromptList()
		msg = request.GET['m']
		topn = 5
		data = json.dumps(searchPromptList.query(msg, topn))
		return HttpResponse(data, content_type='application/json')


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
