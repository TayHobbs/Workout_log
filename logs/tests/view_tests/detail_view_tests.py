from django.test.client import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import Log, Workout, UserProfile


class DetailViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = UserProfile.objects.create(user=User.objects.create_user(username="test.user", password="asdf"))

    def test_user_must_be_logged_in_to_see_detail(self):
        log = Log.objects.create(name="New Log")
        self.user.logs.add(log)
        response = self.client.get(reverse("detail", args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "logs/index.html")

    def test_404_when_user_logged_in_and_log_does_not_exist(self):
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "errors/404.html")

    def test_shows_log_when_user_logged_in_and_log_exists(self):
        self.client.login(username="test.user", password="asdf")
        log = Log.objects.create(name="New Log")
        self.user.logs.add(log)
        response = self.client.get(reverse("detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["log"].name, "New Log")

    def test_workouts_show_on_log_detail_page(self):
        self.client.login(username="test.user", password="asdf")
        workout = Workout.create("New Workout", 3, 5)
        workout.save()
        log = Log.objects.create(name="New Log")
        log.workouts.add(workout)
        log.save()
        self.user.logs.add(log)
        response = self.client.get(reverse("detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["log"].workouts.all()), 1)
