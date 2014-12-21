from django.test import TestCase
from django.contrib.auth.models import User

from logs.forms import UserForm


class UserFormTests(TestCase):

    def test_signup_view(self):
        form = UserForm(
            {
                "username": "test.user",
                "password": "asdf"
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        data_user = User.objects.get(pk=1)
        self.assertEqual(data_user, user)
