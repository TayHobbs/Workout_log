from django.test import TestCase
from django.utils import unittest

from logs.models import Log, Workout


class CreateLogsTests(TestCase):

    def test_can_create_workout(self):
        workout = Workout.create('Bench', 5)
        workout.save()
        print workout.pk
        created = Workout.objects.get(name_of_workout='Bench')
        self.assertEqual(workout, created)
