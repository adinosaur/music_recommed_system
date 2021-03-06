from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'music_recommed_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'accounts.views.login'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^mymusic/', include('mymusic.urls')),
    url(r'^social-music/', include('social_music.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'media/'}),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'static/' }),
    url(r'^favourite/', include('favourite.urls')),
    url(r'^captcha/', include('captcha.urls')),
]
