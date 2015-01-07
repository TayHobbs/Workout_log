from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import UserProfile


class LoginViewTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(user=User.objects.create_user(username="test.user", password="asdf"))

    def test_user_already_signed_in(self):
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("You\'re already signed in!", response.content)
