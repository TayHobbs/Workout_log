from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class ForgottenPasswordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test.user", password="asdf", email="test@test.com")

    def test_send_forgotten_password_email(self):
        response = self.client.get(
            reverse("reset_password", args=["test@test.com"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "logs/reset_password.html")

    def test_change_template_when_email_successfully_sent(self):
        response = self.client.get(
            reverse("reset_password", args=["test@test.com"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user)
        self.assertIn("test.user, your new password is", response.content)
