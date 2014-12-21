from django.test import TestCase
from django.contrib.auth.models import User

from logs.models import Log, Workout, UserProfile
from logs.logging.current_logs import CurrentLogs


class AddToExistingLogTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(user=User.objects.create_user(username="test.user", password="asdf"))
        self.log = Log.objects.create(name="New Log")
        self.user.logs.add(self.log)

    def test_current_logs_class_creates_workout(self):
        request = {"workout": "bench", "sets": 3, "reps": 2, "log": 1}
        CurrentLogs().add_to_existing_log(request)
        created_log = Workout.objects.get(name=request["workout"])
        self.assertEqual(created_log.name, "bench")


class CreateLogsTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(user=User.objects.create_user(username="test.user", password="asdf"))

    def test_log_can_have_multiple_workouts(self):
        workout_one = Workout.create("Bench", 3, 5)
        workout_two = Workout.create("Squat", 3, 5)
        workout_one.save()
        workout_two.save()
        log = Log.objects.create(name="New Log")
        log.workouts.add(workout_one)
        log.workouts.add(workout_two)
        self.assertItemsEqual([workout_one, workout_two], log.workouts.all())

    def test_user_profile_has_logs(self):
        log = Log.objects.create(name="New Log")
        self.user.logs.add(log)
        self.assertEqual(self.user.logs.get(pk=1), log)
