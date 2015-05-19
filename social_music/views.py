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
from models import Attention
from models import SharedMusic
from mymusic.models import Song
import datetime
# Create your views here.
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
		sharedmusic.datetime = datetime.datetime.now()
		sharedmusic.save()
		
	attentions = Attention.objects.filter(user=request.user)
	objQ = Q(user=request.user)
	for attention in attentions:
		objQ |= Q(user=attention.attendedUser)

	sharedMusics = SharedMusic.objects.filter(objQ).order_by("-datetime")
	return  render_to_response(
			'share.html',
			RequestContext(request,{	'sharedMusics':sharedMusics,
										'head': usermessage.head}))