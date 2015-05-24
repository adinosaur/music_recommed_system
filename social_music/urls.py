from django.conf.urls import patterns, url
from social_music import views

urlpatterns = patterns('',
    url(r'^share', views.share),
    url(r'^follow', views.follow),
    url(r'^unfollow', views.unfollow),
    url(r'^comment', views.comment),
    url(r'^remove-comment', views.remove_comment),
    url(r'^create-fav', views.create_fav),
    url(r'^remove-fav', views.remove_fav),
    url(r'^checknews',views.checknews),
)

