from django.conf.urls import patterns, url

from logs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url('^(?P<log_id>\d+)/$', views.detail, name="detail"),
    url('^(?P<log_id>\d+)/create/$', views.create, name="create"),
)
