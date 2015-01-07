from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from logs.models import UserProfile


class MyAccountViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test.user", password="asdf")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_account_name_is_shown_on_account_page(self):
        self.client.login(username="test.user", password="asdf")
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("test.user", response.content)
