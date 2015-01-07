from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import UserProfile


class AddToLogViewTests(TestCase):

    def test_new_user_can_be_created_through_signup_view(self):
        self.assertEqual(len(User.objects.all()), 0)
        data = {"username": "test.user", "password": "asdf"}
        response = self.client.post(reverse("signup"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 1)

    def test_user_not_created_with_bad_credentials(self):
        self.assertEqual(len(User.objects.all()), 0)
        data = {"username": "@)(*&^&*(", "password": "asdf"}
        response = self.client.post(reverse("signup"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 0)

    def test_user_profile_is_created_and_tied_to_new_user(self):
        data = {"username": "test.user", "password": "asdf"}
        response = self.client.post(reverse("signup"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(pk=1)
        self.assertEqual(UserProfile.objects.get(pk=1).user, user)
