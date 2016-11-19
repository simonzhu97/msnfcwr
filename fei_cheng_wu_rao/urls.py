from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fei_cheng_wu_rao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^angel/', include(admin.site.urls)),
    url(r'^', include('liu_yan_ban.urls')),
)
