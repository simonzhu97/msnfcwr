from django.conf.urls import patterns, include, url
from django.contrib import admin
from liu_yan_ban import views
from django.conf.urls import handler404, handler500

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fei_cheng_wu_rao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^angel/', include(admin.site.urls)),
    url(r'^', include('liu_yan_ban.urls')),
)

handler500 = views.catch_error
handler404 = views.catch_error