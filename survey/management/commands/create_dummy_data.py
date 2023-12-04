from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime
from django.contrib.auth.hashers import make_password
from random import getrandbits

from survey.models import Question


class Command(BaseCommand):
    def handle(self, *_, **__):
        fake_pass = make_password("123")
        user_1, _ = User.objects.update_or_create(
            username="user_1", defaults={"password": fake_pass}
        )
        user_2, _ = User.objects.update_or_create(
            username="user_2", defaults={"password": fake_pass}
        )

        if getrandbits(1):
            dummy = localtime() + timedelta(hours=2)
            Question.objects.create(author=user_1, title=f"¿Ya son las {dummy.hour}?")
        else:
            dummy = localtime() + timedelta(hours=1)
            Question.objects.create(
                author=user_2, title=f"¿Cuanto falta para las {dummy.hour}?"
            )
