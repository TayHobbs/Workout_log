from django.test.client import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class LoginViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="test.user", password="asdf")

    def test_user_already_signed_in(self):
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("You\'re already signed in!", response.content)

    def test_user_can_log_in(self):
        request = {"username": self.user.username, "password": self.user.password}
        response = self.client.post(reverse("login"), request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("logs/logs.html")
