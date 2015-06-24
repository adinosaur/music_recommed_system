from django.conf.urls import patterns, url
from favourite import views

urlpatterns = patterns('',
	url(r'^played/$',  views.played),
	url(r'^collected/$',  views.collected),
	url(r'^shared/$',  views.shared),
	
	url(r'^recommend-by-user/$', views.recommendByUser),
	url(r'^recommend-by-song/$', views.recommendBySong),
	url(r'^recommend-by-random/$', views.recommendByRandom),
	
	url(r'^markdwon-play-event/$', views.markdownPlayEvent),
)
