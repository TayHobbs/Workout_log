from django.test.client import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import UserProfile, Log


class MyProfileViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="test.user", password="asdf")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_profile_name_is_shown_on_profile_page(self):
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("profile", args=["test.user"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("test.user", response.content)

    def test_profile_shows_logs(self):
        self.client.login(username="test.user", password="asdf")
        log_one = Log.objects.create(name="Log one")
        log_two = Log.objects.create(name="Log two")
        self.profile.logs.add(log_one, log_two)
        self.profile.save()
        response = self.client.get(reverse("profile", args=["test.user"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["profile"].logs.all()), 2)

    def test_going_to_nonexistant_user_raises_exception_and_redirects(self):
        with self.assertRaises(Exception):
            response = self.client.get(reverse("profile", args=["user"]))
            self.assertIn("Page Not Found", response.content)
