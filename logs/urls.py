from django.conf.urls import patterns, url

from logs import views

urlpatterns = patterns(
    "",
    url(r"^$", views.index, name="index"),
    url(r"^logs/$", views.logs, name="logs"),
    url(r"^signup/$", views.signup, name="signup"),
    url(r"^login/$", views.user_login, name="login"),
    url(r"^logout/$", views.user_logout, name="logout"),
    url("^logs/(?P<log_id>\d+)/$", views.detail, name="detail"),
    url("^create_new_log/$", views.create_new_log, name="create"),
    url("^add_to_log/$", views.add_to_log, name="add_to_log"),
    url(r"^profile/$", views.user_profile, name="profile"),
    url(r"^log_list/$", views.LogList.as_view(), name="log_list"),
    url("^log_detail/(?P<pk>[0-9]+)/$", views.LogDetail.as_view(), name="log_detail"),
    url(r"^workout_list/$", views.WorkoutList.as_view(), name="workout_list"),
    url("^workout_detail/(?P<pk>[0-9]+)/$", views.WorkoutDetail.as_view(), name="workout_detail"),
    url(r"^user_profile_list/$", views.UserProfileList.as_view(), name="user_profile_list"),
    url("^user_profile_detail/(?P<pk>[0-9]+)/$", views.UserProfileDetail.as_view(), name="user_profile_detail"),
)
