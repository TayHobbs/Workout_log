from django.test import TestCase
from django.utils import unittest
from django.contrib.auth.models import User

from logs.models import Log, Workout


class CreateLogsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test.user")

    def test_log_can_have_multiple_workouts(self):
        workout_one = Workout.create('Bench', 5)
        workout_two = Workout.create('Squat', 5)
        workout_one.save()
        workout_two.save()
        log = Log.objects.create(user=self.user)
        log.workouts.add(workout_one)
        log.workouts.add(workout_two)
        self.assertItemsEqual([workout_one, workout_two], log.workouts.all())

    def test_log_has_a_user(self):
        log = Log.objects.create(user=self.user)
        self.assertEqual(log.user, self.user)
