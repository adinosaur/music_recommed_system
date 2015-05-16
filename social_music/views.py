from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Attention
from models import SharedMusic
# Create your views here.

@login_required
def attention(request):
	if request.method == 'POST':
		attendedUser = request.POST['attendedUser']
		try:
			Attention.objects.get(user=request.user, attendedUser=attendedUser).count()
		except Attention.DoesNotExist:
			attention = Attention()
			attention.user = request.user
			attention.attendedUser = attendedUser
			attention.save()
			return HttpResponse("attending success!")
		else:
			return HttpResponse("attending failed!")

@login_required
def share(request):
	if request.method == 'GET':
		return HttpResponse("share request")