from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

from logs.views import WorkoutDetail
from logs.models import Log, Workout, UserProfile
from logs.serializers import WorkoutSerializer


class WorkoutAPITests(TestCase):

    def setUp(self):
        self.workout = Workout.objects.create(name="New Workout", sets=3, reps=5)
        self.user = User.objects.create_user(username="test.user", password="asdf")
        self.log = Log.objects.create(name="New Log")
        self.log.workouts.add(self.workout)
        self.log.save()
        self.profile = UserProfile.objects.create(user=self.user)
        self.profile.logs.add(self.log)
        self.factory = APIRequestFactory()

    def test_serialize_workout(self):
        serialized_dict = WorkoutSerializer(self.workout)
        expected_dict = {'id': 1, 'name': u'New Workout', 'sets': 3, 'reps': 5}
        self.assertEqual(serialized_dict.data, expected_dict)

    def test_workout_list_view_returns_all_workouts(self):
        view = WorkoutDetail.as_view()
        request = self.factory.get(reverse("workout_detail", args=[1]))
        response = view(request, pk='1')
        response.render()
        expected = '{"id": 1, "name": "New Workout", "sets": 3, "reps": 5}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected)
