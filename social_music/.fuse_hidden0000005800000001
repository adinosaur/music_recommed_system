from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
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
	if request.method == 'GET':
		attentions = Attention.objects.filter(user = request.user)
		sharedmusics = []
		for attention in attentions:
			try:
				sharedmusic = SharedMusic.objects.filter(user= attention.attendedUser)
				for everymusic in sharedmusic:
					sharedmusics.append(everymusic)
			except SharedMusic.DoesNotExist:
				print "no sharedmusics data"		
		try:
			songid = request.GET['id']
			song = Song.objects.get(id = songid)
		except Exception,e:
			return render_to_response(
			'share.html', 
			RequestContext(request, {'sharedmusics':sharedmusics}))
		return render_to_response(
			'share.html', 
			RequestContext(request, {'song': song,'sharedmusics':sharedmusics}))
	if request.method == 'POST':
		comment = request.POST['comment']
		songid = request.GET['id']
		song = Song.objects.get(id = songid)
		sharedmusic = SharedMusic()
		sharedmusic.user = request.user
		sharedmusic.comment = comment
		sharedmusic.song = song
		sharedmusic.datetime = datetime.datetime.now()
		sharedmusic.save()
		attentions = Attention.objects.filter(user = request.user)
		sharedmusics = []
		for attention in attentions:
			try:
				sharedmusic = SharedMusic.objects.filter(user= attention.attendedUser)
				for everymusic in sharedmusic:
					sharedmusics.append(everymusic)
			except SharedMusic.DoesNotExist:
				print "no sharedmusics"	
		return  render_to_response(
			'share.html',
			RequestContext(request,{'song': song,'sharedmusics':sharedmusics}))
