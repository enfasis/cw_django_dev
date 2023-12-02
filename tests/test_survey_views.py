from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from survey.constants import AnswerValue, LikeValue
from survey.models import Question

from tests.factories import AnswerFactory, LikeFactory, QuestionFactory, UserFactory


def test_create(client: Client):
    res = client.post(
        reverse("survey:question-create"), data={"title": "fake", "description": "des"}
    )
    assert res.status_code == 302  # Redirects

    question = Question.objects.first()

    assert question

    assert question.title == "fake"
    assert question.description == "des"


def get_questions(client: Client):
    res = client.get(reverse("survey:question-list"))
    assert res.status_code == 200
    context: dict = res.context[-1]
    return context["object_list"]


def test_list_unthenticated_view():
    client = Client()

    QuestionFactory.create_batch(3)

    questions = get_questions(client)

    assert len(questions) == 3

    for question in questions:
        assert not hasattr(question, "user_dislikes")
        assert not hasattr(question, "user_likes")
        assert not hasattr(question, "user_value")


def test_list_no_answers_no_likes(client: Client):
    QuestionFactory.create_batch(3)

    questions = get_questions(client)

    for question in questions:
        assert question.user_dislikes is False
        assert question.user_likes is False
        assert question.user_value is None


def test_list_answer_value(user: User, client: Client):
    AnswerFactory.create(author=user, value=AnswerValue.Regular)

    questions = get_questions(client)

    assert len(questions) == 1

    assert questions[0].user_value == AnswerValue.Regular


def test_list_like_value(user: User, client: Client):
    LikeFactory.create(author=user, value=LikeValue.Disliked)

    questions = get_questions(client)

    assert len(questions) == 1

    assert not questions[0].user_likes
    assert questions[0].user_dislikes


def test_ranking_order(client: Client):
    question_1 = QuestionFactory.create(ranking=10)
    question_2 = QuestionFactory.create(ranking=100)

    questions = get_questions(client)

    assert question_1 == questions[1]
    assert question_2 == questions[0]


def update_question(user, question, value):
    client = Client()
    client.force_login(user)

    url_name = "api:answer_question"
    if value in LikeValue:
        url_name = "api:like_or_dislike_question"

    res = client.post(
        reverse(url_name),
        data={"question": question.pk, "value": value},
        content_type="application/json",
    )
    question.refresh_from_db()

    assert res.status_code == 200


def test_interaction():
    question = QuestionFactory.create()

    # Today questions start with 10 points
    assert question.ranking == 10

    # Every answer sums 10
    for user in UserFactory.create_batch(6):
        update_question(user, question, AnswerValue.VeryHigh)

    assert question.ranking == 10 + 6 * 10

    # Every like sums 5
    for user in UserFactory.create_batch(2):
        update_question(user, question, LikeValue.Liked)

    assert question.ranking == 10 + 6 * 10 + 2 * 5

    # Every dislike subtracts 3
    update_question(UserFactory.create(), question, LikeValue.Disliked)

    assert question.ranking == 10 + 6 * 10 + 2 * 5 - 3


def test_interaction_double_answer_same_ranking(user: User):
    question = QuestionFactory.create()

    assert question.ranking == 10

    update_question(user, question, AnswerValue.VeryHigh)
    assert question.ranking == 10 + 10

    update_question(user, question, AnswerValue.Low)
    assert question.ranking == 10 + 10


def test_interaction_double_like_same_ranking(user: User):
    question = QuestionFactory.create()

    assert question.ranking == 10

    update_question(user, question, LikeValue.Liked)
    assert question.ranking == 10 + 5

    update_question(user, question, LikeValue.Liked)
    assert question.ranking == 10 + 5

    update_question(user, question, LikeValue.Disliked)
    assert question.ranking == 10 - 3

    update_question(user, question, LikeValue.Disliked)
    assert question.ranking == 10 - 3

    update_question(user, question, LikeValue.Liked)
    assert question.ranking == 10 + 5
