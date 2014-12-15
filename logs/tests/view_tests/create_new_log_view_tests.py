from django.test.client import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AddToLogViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="test.user", password="asdf")

    def test_new_log_is_created_and_workout_is_added_to_it(self):
        data = {"workout": "New Workout", "reps": 5, "log": "New Log"}
        self.client.login(username="test.user", password="asdf")
        response = self.client.post(reverse("create"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "logs/logs.html")
        self.assertEqual(len(response.context["logs"]), 1)
