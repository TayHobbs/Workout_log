import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import Log, UserProfile


class LogsViewTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(
            user=User.objects.create_user(
                username="test.user", password="asdf"))

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
        log = Log.objects.create(name="New Log")
        self.user.logs.add(log)
        response = self.client.get(reverse("logs"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["logs"]), 1)

    def test_logs_are_ordered_by_date(self):
        self.client.login(username="test.user", password="asdf")
        log_one = Log.objects.create(
            name="Second Log", date=datetime.date(2013, 12, 02))
        log_two = Log.objects.create(name="First Log")
        self.user.logs.add(log_one, log_two)
        response = self.client.get(reverse("logs"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["logs"][0].name, 'First Log')
