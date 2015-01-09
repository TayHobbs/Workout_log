import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

from logs.views import UserProfileViewSet
from logs.models import Log, UserProfile
from logs.serializers import UserProfileSerializer


class UserProfileAPITests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test.user", password="asdf")
        self.log = Log.objects.create(
            name="New Log", date=datetime.date(2013, 12, 02))
        self.profile = UserProfile.objects.create(user=self.user)
        self.profile.logs.add(self.log)
        self.factory = APIRequestFactory()

    def test_serialize_workout(self):
        serialized_dict = UserProfileSerializer(self.profile)
        expected_dict = {
            'id': 1,
            'user': 1,
            'logs': [1],
            'profile_picture': u'',
            'twitter': u'',
            'facebook': u'',
            'website': u''
        }
        self.assertEqual(serialized_dict.data, expected_dict)

    def test_workout_list_view_returns_all_workouts(self):
        view = UserProfileViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get("/api/profile_api/")
        response = view(request, pk='1')
        response.render()
        expected = '{"id": 1, "user": 1, "logs": [1], "profile_picture": "", "twitter": "", "facebook": "", "website": ""}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)
