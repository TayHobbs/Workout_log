import json
import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import Log, UserProfile, Workout


class AddToLogViewTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(
            user=User.objects.create_user(
                username="test.user", password="asdf"))

    def test_workout_is_added_to_log(self):
        log = Log.objects.create(name="New Log")
        self.user.logs.add(log)
        data = {"workout": "New Workout", "sets": 3, "reps": 5, "log": log.pk}
        self.client.login(username="test.user", password="asdf")
        response = self.client.post(reverse("add_to_log"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        log_workout = response.context["log"].workouts.get(name="New Workout")
        self.assertEqual(log_workout.name, "New Workout")

    def test_shows_last_workouts_sorted_by_date(self):
        log = Log.objects.create(name="New Log")
        workout_one = Workout.create("New Workout", 3, 5)
        workout_two = Workout.create("New Workout Two", 3, 5)
        workout_two = Workout.create("New Workout Two", 3, 5)
        workout_two.save()
        workout_two.last_date_added = datetime.date(2016, 12, 02)
        workout_one.save()
        log.workouts.add(workout_one, workout_two)
        log.save()
        self.user.logs.add(log)
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("add_to_log"))
        self.assertEqual(response.status_code, 200)
        expected_json = '[{"id": 1, "name": "New Workout Two", "sets": 3, "reps": 5}, {"id": 2, "name": "New Workout", "sets": 3, "reps": 5}]'
        self.assertEqual(response.content, expected_json)

    def test_only_shows_last_twenty_workouts(self):
        self.client.login(username="test.user", password="asdf")
        log = Log.objects.create(name="New Log")
        for i in range(0, 21):
            workout = Workout.objects.create(name="New Workout", sets=3, reps=5)
            workout.save()
            log.workouts.add(workout)
        log.save()
        self.user.logs.add(log)
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("add_to_log"))
        self.assertEqual(response.status_code, 200)
        expected = json.loads(response.content)
        self.assertEqual(len(expected), 20)
