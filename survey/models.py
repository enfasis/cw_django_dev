from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import (
    BooleanField,
    DateField,
    ForeignKey,
    IntegerField,
    TextField,
    PositiveIntegerField,
    CASCADE,
    CharField,
    Model,
)
from django.db.models.indexes import Index
from django.db.models.constraints import UniqueConstraint

from .constants import LikeValue, AnswerValue


class Question(Model):
    class Meta:
        # Default django btree index that produces sorted output
        indexes = [Index(fields=["ranking"])]

    created = DateField("Creada", auto_now_add=True)
    author = ForeignKey(
        get_user_model(),
        related_name="questions",
        verbose_name="Pregunta",
        on_delete=CASCADE,
    )
    title = CharField("Título", max_length=200)
    description = TextField("Descripción")

    ranking = IntegerField(default=10)

    # flag field to update the ranking with a cron job
    is_from_today = BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("survey:question-edit", args=[self.pk])


class Answer(Model):
    class Meta:
        constraints = [
            UniqueConstraint(fields=["question", "author"], name="unique_answer"),
        ]

    question = ForeignKey(
        Question, related_name="answers", verbose_name="Pregunta", on_delete=CASCADE
    )
    author = ForeignKey(
        get_user_model(),
        related_name="answers",
        verbose_name="Autor",
        on_delete=CASCADE,
    )
    value = PositiveIntegerField(
        "Respuesta", choices=AnswerValue.choices, default=AnswerValue.NoAnswer
    )


class Like(Model):
    class Meta:
        constraints = [
            UniqueConstraint(fields=["question", "author"], name="unique_like"),
        ]

    question = ForeignKey(
        Question, related_name="likes", verbose_name="Pregunta", on_delete=CASCADE
    )
    author = ForeignKey(
        get_user_model(), related_name="likes", verbose_name="Autor", on_delete=CASCADE
    )
    value = CharField(choices=LikeValue.choices, max_length=9)
