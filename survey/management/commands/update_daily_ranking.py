from django.core.management.base import BaseCommand
from django.utils.timezone import localdate
from django.db.models import F

from survey.models import Question


class Command(BaseCommand):
    def handle(self, *_, **__):
        Question.objects.filter(is_from_today=True, created__lt=localdate()).update(
            is_from_today=False, ranking=F("ranking") - 10
        )
