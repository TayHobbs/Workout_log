from django.conf.urls import patterns, url

from logs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^logs/$', views.logs, name='logs'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url('^(?P<log_id>\d+)/$', views.detail, name="detail"),
    url('^(?P<log_id>\d+)/create/$', views.create, name="create"),
)
