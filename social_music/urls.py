from django.conf.urls import patterns, url
from social_music import views

urlpatterns = patterns('',
    url(r'^share', views.share),
    url(r'^follow', views.follow),
)

