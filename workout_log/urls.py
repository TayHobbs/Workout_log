from django.conf.urls import patterns, include, url

from django.contrib import admin
from workout_log import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'workout_log.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('logs.urls')),
    url(r'^logs/', include('logs.urls', namespace="logs")),
    url(r'^admin/', include(admin.site.urls)),
)
