from django.conf.urls import patterns, url
from mymusic import views

urlpatterns = patterns('',
    url(r'^song-lib',  views.song_lib),
    url(r'^play',  views.play),
)
