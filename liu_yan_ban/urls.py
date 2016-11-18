from django.conf.urls import patterns, url

from liu_yan_ban import views

urlpatterns = patterns('',
    url(r'^home/$', views.home, name='Home'),
    url(r'^$', views.index, name='Index'),
    url(r'^home/$', views.home, name='Home'),
    url(r'^success/$', views.success, name='Success'),
    url(r'^submit/$', views.submit, name='Submit'),
    url(r'^show/(?P<comment_id>\d+)/$', views.show, name='Show'),
    url(r'^confirmation/(?P<trans_id>\d+)/$', views.confirmation, name='Confirmation'),
    url(r'^dismiss/(?P<comment_id>\d+)/$', views.dismiss, name='Dismiss'),
    url(r'^top/(?P<comment_id>\d+)/(?P<option>\d+)/$', views.top, name='Top'),
    url(r'^like/(?P<comment_id>\d+)/$', views.like, name='Like'),
    url(r'^view/$', views.view, name='View'),
    url(r'^flower/self/$', views.flower_self, name='FlowerSelf'),
	url(r'^flower/msn/$', views.flower_msn, name='FlowerMSN'),
    url(r'^flower/$', views.delivery, name='Delivery'),
    url(r'^handle/(?P<trans_id>\d+)/$', views.handle, name='Handle'),
    url(r'^process/(?P<trans_id>\d+)/$', views.process, name='Process'),
    url(r'^flower/submit/self/$', views.flower_self_submit, name='FlowerSubmitSelf'),
    url(r'^flower/submit/msn/$', views.flower_msn_submit, name='FlowerSubmitMSN'),
    url(r'^transaction/cancel/(?P<trans_id>\d+)/$', views.cancel, name='Cancel'),
    url(r'^transaction/confirm/(?P<trans_id>\d+)/$', views.confirm, name='Confirm'),
    url(r'^dm/(?P<user_id>\d+)/$', views.direct_message, name='DM'),
    url(r'^dm/$', views.direct_message_all, name='DMAll'),
    url(r'^', views.error, name='Error'),
)