import random
import string

from django.contrib.auth.models import User
from django.core.mail import send_mail


class ProfileNotFound(Exception):
    pass


class ProfileManager(object):

    def change_profile_pic(self, account, image):
        account.profile_picture = image
        account.save()

    def send_forgotten_password_email(self, user):
        email_subject = "Workout Logger: Forgotten Password"
        email_body = """
            Hello! Someone has requested a password reset on your account, if
            this was you, click the link below to reset your password
            http://127.0.0.1:8000/account/reset-password/{}/\n
            If this wasn't you, ignore this email.
        """.format(user.email)
        send_mail(
            email_subject,
            email_body,
            'hobbstay@gmail.com',
            [user.email],
            fail_silently=False
        )

    def reset_password(self, email):
        new_password = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(8))
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user, new_password
