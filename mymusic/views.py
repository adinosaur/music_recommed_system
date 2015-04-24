from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Song
# Create your views here.

@login_required
def song_lib(request):
    return render_to_response('index.html', RequestContext(request, {}))

@login_required
def play(request):
    if request.method == 'GET':
        song_id = request.GET['id']
        _song = Song.objects.get(pk=song_id)
        print _song.pic_link
        return render_to_response('play.html', RequestContext(request, {'song':_song})) 

