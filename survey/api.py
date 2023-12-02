from ninja import Router
from ninja import Schema
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from django.db.models import F
from typing import Literal
from survey.constants import LikeValue
from survey.models import Like, Question, Answer

router = Router(auth=django_auth)


class AnswerSchema(Schema):
    question: int
    value: int


class OkSchema(Schema):
    ok: Literal[True] = True


class LikeSchema(Schema):
    question: int
    value: Literal["like", "dislike"]


@router.post("/answer", response=OkSchema)
@atomic
def answer_question(request, data: AnswerSchema):
    question = get_object_or_404(Question, pk=data.question)
    _, created = Answer.objects.update_or_create(
        question=question, author=request.user, defaults={"value": data.value}
    )
    if created:
        question.ranking = F("ranking") + 10
        question.save()
    return OkSchema()


@router.post("/like", response=OkSchema)
def like_or_dislike_question(request, data: LikeSchema):
    question = get_object_or_404(Question, pk=data.question)
    like, created = Like.objects.get_or_create(
        question=question, author=request.user, defaults={"value": data.value}
    )

    points = 0

    if created or Like.objects.filter(pk=like.pk).exclude(value=data.value).update(
        value=data.value
    ):
        points = 5 if data.value == LikeValue.Liked else -3

    question.ranking = F("ranking") + points
    question.save()
    return OkSchema()
