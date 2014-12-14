from django.test.client import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import Log, Workout
from logs.logging.current_logs import CurrentLogs


class AddToLogViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="test.user", password="asdf")

    def test_workout_is_added_to_log(self):
        log = Log.objects.create(user=self.user, name="New Log")
        data = {"workout": "New Workout", "reps": 5, "log": log.pk}
        self.client.login(username="test.user", password="asdf")
        response = self.client.post(reverse("add_to_log"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        log_workout = response.context["log"].workouts.get(name="New Workout")
        self.assertEqual(log_workout.name, "New Workout")
