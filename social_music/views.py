#coding=utf8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from accounts.models import UserMessage 
from django.db.models import Q
from mymusic.models import Song

from mymusic.pages_assistant import Page_Assistant
from favourite.algorithm import update_favourite
from favourite.lastSong import getLastPlayedSong

from models import Attention
from models import SharedMusic
from models import SharedMusicComment
from models import FavSharedMusic
from models import UserNews
from datetime import datetime
from django.core import serializers
import json

@csrf_exempt
@login_required
def follow(request):
	if request.method == 'POST':
		
		uid = request.POST['uid']
		print "[INFO]social-music.views.follow: uid=%s" %(uid)
		attendedUser = User.objects.get(pk=uid)
		try:
			Attention.objects.get(user=request.user, attendedUser=attendedUser)
		except Attention.DoesNotExist:
			attention = Attention()
			attention.user = request.user
			attention.attendedUser = attendedUser
			attention.save()
			print "[INFO]social-music.views.follow: <%s> following <%s> success." %(request.user, attendedUser)
			return HttpResponse("following success!")
		else:
			print "[ERROR]social-music.views.follow: <%s> following <%s> failure." %(request.user, attendedUser)
			return HttpResponse("following failure!")

@csrf_exempt
@login_required
def unfollow(request):
	if request.method == 'POST':
		
		uid = request.POST['uid']
		print "[INFO]social-music.views.unfollow: uid=%s" %(uid)
		attendedUser = User.objects.get(pk=uid)
		try:
			attention = Attention.objects.get(user=request.user, attendedUser=attendedUser)
			attention.delete()
			print "[INFO]social-music.views.unfollow: <%s> unfollow <%s> success." %(request.user, attendedUser)
			return HttpResponse("unfollow success!")
		except Attention.DoesNotExist:
			print "[ERROR]social-music.views.unfollow: <%s> unfollow <%s> failure." %(request.user, attendedUser)
			return HttpResponse("unfollowi failure!")

@login_required
def share(request):
	usermessage = UserMessage.objects.get(user=request.user)
	if request.method == 'POST':
		comment = request.POST['share_comment']
		songid = request.POST['song_id']
		song = Song.objects.get(id=songid)
		print "[INFO]social-music.views.share: share(song=%s)" %(song)

		sharedmusic = SharedMusic()
		sharedmusic.user = request.user
		sharedmusic.comment = comment
		sharedmusic.song = song
		sharedmusic.datetime = datetime.now()
		sharedmusic.save()
		
		behave = 'shared'
		update_favourite(sharedmusic.user.pk, sharedmusic.song.pk, behave)
		print "[INFO]social-music.views.share: user_id:%s, song_id:%s, %s" %(sharedmusic.user.pk, sharedmusic.song.pk, behave)

	attentions = Attention.objects.filter(user=request.user)
	objQ = Q(user=request.user)
	for attention in attentions:
		objQ |= Q(user=attention.attendedUser)

	sharedMusics = SharedMusic.objects.filter(objQ).order_by("-datetime")
	sharedMusicCount = SharedMusic.objects.filter(user=request.user).count()
	followingCount = len(attentions)
	followedCount = Attention.objects.filter(attendedUser=request.user).count()
	for sharedMusic in sharedMusics:
		sharedMusic.comments = SharedMusicComment.objects.filter(sharedMusic=sharedMusic).order_by("datetime")
		for comment in sharedMusic.comments:
			comment.datetime = comment.datetime.strftime("%Y/%m/%d %H:%M")
		sharedMusic.datetime = sharedMusic.datetime.strftime("%Y/%m/%d %H:%M")

	#读取新消息的数量
	newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
	
	#上一次播放的音乐
	last_song = getLastPlayedSong(request.user)
	
	return  render_to_response(
			'share.html',
			RequestContext(request,{	'last_song': last_song,
										'newsCount': newsCount,
										'sharedMusics':sharedMusics,
										'head': usermessage.head,
										'sharedMusicCount': sharedMusicCount,
										'followingCount': followingCount,
										'followedCount': followedCount}))

@login_required
def share_json(request):
	"""http://127.0.0.1:8000/social-music/json/share%EF%BC%9Fp=1/"""
	if request.method == 'GET':
		print "[INFO]social-music.views.share_json"
		usermessage = UserMessage.objects.get(user=request.user)
		attentions = Attention.objects.filter(user=request.user)
		objQ = Q(user=request.user)
		for attention in attentions:
			objQ |= Q(user=attention.attendedUser)

		#将网页分页展示
		p = request.GET.get('p', '1')
		page_assistant = Page_Assistant(count=SharedMusic.objects.filter(objQ).count(), page_size=5)
		pre_page = page_assistant.get_pre_page_no(int(p))
		cur_page = int(p)
		nex_page = page_assistant.get_nex_page_no(int(p))
		page_nums = page_assistant.get_pages_list(cur_page)
		b, e = page_assistant.get_objects_by_pageno(cur_page)
		sharedMusics = SharedMusic.objects.filter(objQ).order_by("-datetime")[b:e]
		
		sharedMusicCount = SharedMusic.objects.filter(user=request.user).count()
		followingCount = len(attentions)
		followedCount = Attention.objects.filter(attendedUser=request.user).count()
		
		for sharedMusic in sharedMusics:
			sharedMusic.comments = SharedMusicComment.objects.filter(sharedMusic=sharedMusic).order_by("datetime")
			#for comment in sharedMusic.comments:
			#	comment.datetime = comment.datetime.strftime("%Y/%m/%d %H:%M")
			#sharedMusic.datetime = sharedMusic.datetime.strftime("%Y/%m/%d %H:%M")

		#读取新消息的数量
		newsCount = UserNews.objects.filter(toUser=request.user, seen=False).count()
		
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)

		responseDict = dict()
		responseDict['last_song'] = last_song
		responseDict['newsCount'] = newsCount
		responseDict['sharedMusics'] = json.loads(serializers.serialize('json', sharedMusics))
		responseDict['head'] = usermessage.head
		responseDict['sharedMusicCount'] = sharedMusicCount
		responseDict['followingCount'] = followingCount
		responseDict['followedCount'] = followedCount
		data = json.dumps(responseDict)
		return HttpResponse(data, content_type='application/json')

@csrf_exempt
@login_required
def comment(request):
	if request.method == 'POST':
		sharedMusicComment = SharedMusicComment()
		try:
			sharedMusicID = request.POST['comment_id']
		except KeyError, e:
			print "[INFO]social-music.views.comment: wrong sharedMusicID!"
			print e

		print "[INFO]social-music.views.comment: sharedMusicID=%s" %request.POST['comment_id']
		print "[INFO]social-music.views.comment: comment=%s" %request.POST['comment']
		print request.POST

		sharedMusicComment.sharedMusic = SharedMusic.objects.get(pk=sharedMusicID)
		sharedMusicComment.user = request.user
		sharedMusicComment.comment = request.POST['comment']
		sharedMusicComment.datetime = datetime.now()
		sharedMusicComment.save()

		print sharedMusicComment.sharedMusic.pk
		print sharedMusicComment.pk
		print sharedMusicComment.comment

		#将新评论添加至消息系统中
		userNews = UserNews()
		userNews.fromUser = request.user
		userNews.toUser = sharedMusicComment.sharedMusic.user
		userNews.newsType = 0
		userNews.newsID = sharedMusicComment.pk
		userNews.save()

		return HttpResponseRedirect('/social-music/share/')

@csrf_exempt
@login_required
def remove_comment(request):
	if request.method == 'POST':
		sharedMusicCommentID = request.POST['comment_id']
		sharedMusicComment = SharedMusicComment.objects.get(pk=sharedMusicCommentID)
		if request.user == sharedMusicComment.user:
			print "[INFO]social-music.views.remove_comment: commentID=%s" %sharedMusicCommentID

			#同时还要删除UserNews中的评论（newsType=0）消息
			userNews = UserNews.objects.get(newsType=0, newsID=sharedMusicCommentID)
			userNews.delete()

			sharedMusicComment.delete()
		else:
			print "[ERROR]social-music.views.remove_comment: cannot remove commentID=%s" %sharedMusicCommentID
		return HttpResponseRedirect('/social-music/share/')

@csrf_exempt
@login_required
def create_fav(request):
	if request.method == 'POST':
		try:
			sharedMusicID = request.POST['id']
			sharedMusic = SharedMusic.objects.get(pk=sharedMusicID)
			try:
				FavSharedMusic.objects.get(sharedMusic=sharedMusic, user=request.user)
				print "[INFO]social-music.views.create_fav: alreadly done"
			except FavSharedMusic.DoesNotExist:
				favSharedMusic = FavSharedMusic()
				favSharedMusic.sharedMusic = sharedMusic
				favSharedMusic.user = request.user
				favSharedMusic.save()

				#将新的点赞消息添加至消息系统中
				userNews = UserNews()
				userNews.fromUser = request.user
				userNews.toUser = sharedMusic.user
				userNews.newsType = 1
				userNews.newsID = favSharedMusic.pk
				userNews.save()
			
				print "[INFO]social-music.views.create_fav: success"
		except Exception, e:
			print e
		return HttpResponseRedirect('/social-music/share/')

@csrf_exempt
@login_required
def remove_fav(request):
	if request.method == 'POST':
		sharedMusicID = request.POST['id']
		sharedMusic = SharedMusic.objects.get(pk=sharedMusicID)
		favSharedMusic = FavSharedMusic.objects.get(sharedMusic=sharedMusic, user=request.user)

		#同时还要删除UserNews中的点赞（newsType=1）消息
		userNews = UserNews.objects.get(newsType=1, newsID=sharedMusicID)
		userNews.delete()

		favSharedMusic.delete()
		print "[INFO]social-music.views.remove_fav: success"
		return HttpResponseRedirect('/social-music/share/')

@login_required
def message(request):
	if request.method == 'GET':
		usermessage = UserMessage.objects.get(user=request.user)

		if 'IsComment' in request.GET:
			newsType = 0
			news = UserNews.objects.filter(toUser=request.user, newsType=0).order_by("-datetime")
			for n in news:
				n.obj = SharedMusicComment.objects.get(pk=n.newsID)
				n.seen = True
				n.save()
				n.datetime = n.datetime.strftime("%Y/%m/%d %H:%M")

		if 'IsFavour' in request.GET:
			newsType = 1
			news = UserNews.objects.filter(toUser=request.user, newsType=1).order_by("-datetime")
			for n in news:
				n.obj = FavSharedMusic.objects.get(id=n.newsID)
				n.seen = True
				n.save()
				n.datetime = n.datetime.strftime("%Y/%m/%d %H:%M")
				
		#上一次播放的音乐
		last_song = getLastPlayedSong(request.user)

		return render_to_response(
			'messages.html',
			RequestContext(request,{	'last_song': last_song,
										'head': usermessage.head,
										'newsList': news,
										'newsType': newsType}))
