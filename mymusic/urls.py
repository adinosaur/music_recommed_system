from django.conf.urls import patterns, url
from mymusic import views

urlpatterns = patterns('',
    url(r'^song-lib',  views.song_lib),
    url(r'^play',  views.play),
    url(r'^create-fav', views.create_fav),
    url(r'^remove-fav', views.remove_fav),
    url(r'^singer', views.singer),
    url(r'^search-singer', views.search_singer),
    url(r'^search-song', views.search_song),
    url(r'^comment', views.comment),
    url(r'^favour-comment', views.favour_comment),
    url(r'^cancel-favour-comment', views.cancel_favour_comment),
)
