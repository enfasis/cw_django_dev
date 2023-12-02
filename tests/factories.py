from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory import Faker, Sequence, SubFactory
from survey.constants import AnswerValue, LikeValue

from survey.models import Answer, Like, Question


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["username"]
        skip_postgeneration_save = True

    username = Sequence(lambda n: "u" + str(10_000_000 + n))


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question
        django_get_or_create = ["title", "author"]
        skip_postgeneration_save = True

    author = SubFactory(UserFactory)
    title = Faker("name")
    description = Faker("text")


class BaseRelatedQuestionFactory(DjangoModelFactory):
    class Meta:
        django_get_or_create = ["question", "author"]
        skip_postgeneration_save = True
        abstract = True

    question = SubFactory(QuestionFactory)
    author = SubFactory(UserFactory)


class AnswerFactory(BaseRelatedQuestionFactory):
    class Meta:
        model = Answer

    value = Faker("random_element", elements=AnswerValue.values)


class LikeFactory(BaseRelatedQuestionFactory):
    class Meta:
        model = Like

    value = Faker("random_element", elements=LikeValue.values)
