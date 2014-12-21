from django.conf.urls import patterns, url, include

from rest_framework.routers import SimpleRouter

from logs import views
from logs.views import *

router = SimpleRouter()
router.register(r'api/workout_api', views.WorkoutViewSet)
router.register(r'api/profile_api', views.UserProfileViewSet)
router.register(r'api/log_api', views.LogViewSet)
router.register(r'api/users', views.UserViewSet)

urlpatterns = patterns(
    "",
    url(r"^", include(router.urls)),
    url(r"^index/$", views.index, name="index"),
    url(r"^logs/$", Logs.as_view(), name="logs"),
    url(r"^signup/$", Signup.as_view(), name="signup"),
    url(r"^login/$", UserLogin.as_view(), name="login"),
    url(r"^logout/$", views.user_logout, name="logout"),
    url("^logs/(?P<log_id>\d+)/$", Detail.as_view(), name="detail"),
    url("^create_new_log/$", CreateNewLog.as_view(), name="create"),
    url("^add_to_log/$", AddToLog.as_view(), name="add_to_log"),
    url(r"^profile/$", Profile.as_view(), name="profile"),
)
