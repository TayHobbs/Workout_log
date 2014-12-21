from django.test import TestCase
from django.contrib.auth.models import User

from logs.models import Log, UserProfile


class UserProfileTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test.user")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_profile_has_user(self):
        self.assertEqual(self.profile.user, self.user)

    def test_profile_has_logs(self):
        self.client.login(username="test.user", password="asdf")
        log_one = Log.objects.create(name="Log one")
        log_two = Log.objects.create(name="Log two")
        self.profile.logs.add(log_one, log_two)
        self.profile.save()
        profile = UserProfile.objects.get(pk=1)
        self.assertEqual(len(profile.logs.all()), 2)
