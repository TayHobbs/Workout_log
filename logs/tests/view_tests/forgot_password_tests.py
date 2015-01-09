from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User


class ForgottenPasswordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test.user", password="asdf", email="test@test.com")

    def test_send_forgotten_password_email(self):
        data = {"email": "test@test.com"}
        email_body = """
            Hello! Someone has requested a password reset on your account, if
            this was you, click the link below to reset your password
            http://127.0.0.1:8000/account/reset-password/test@test.com/\n
            If this wasn't you, ignore this email.
        """
        response = self.client.post(reverse("forgot_password"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Workout Logger: Forgotten Password")
        self.assertEqual(mail.outbox[0].body, email_body)

    def test_change_template_when_email_successfully_sent(self):
        data = {"email": "test@test.com"}
        response = self.client.post(reverse("forgot_password"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "Your password reset email has been sent", response.content)

    def test_dont_send_email_when_no_user_email_provided(self):
        response = self.client.post(reverse("forgot_password"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_template_changed_and_email_not_sent_when_bad_email_provided(self):
        data = {"email": "invalid@email.com"}
        response = self.client.post(
            reverse("forgot_password"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn(
            "I'm sorry the email you entered wasn't found. Please try again.",
            response.content)
