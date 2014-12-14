import datetime

from django.test.client import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import Log, Workout
from logs.logging.current_logs import CurrentLogs


class LogsViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="test.user", password="asdf")

    def test_logs_view_when_user_is_not_logged_in(self):
        response = self.client.get(reverse("logs"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "You are not signed in")

    def test_logs_view_when_user_is_logged_in(self):
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("logs"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logout", response.content)

    def test_logs_view_shows_logs_when_logs_are_created(self):
        self.client.login(username="test.user", password="asdf")
        Log.objects.create(user=self.user, name="New Log")
        response = self.client.get(reverse("logs"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["logs"]), 1)

    def test_logs_are_ordered_by_date(self):
        self.client.login(username="test.user", password="asdf")
        Log.objects.create(user=self.user, name="Second Log", date=datetime.date(2013, 12, 02))
        Log.objects.create(user=self.user, name="First Log")
        response = self.client.get(reverse("logs"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["logs"][0].name, 'First Log')
