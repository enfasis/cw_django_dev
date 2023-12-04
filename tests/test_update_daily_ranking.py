from datetime import timedelta
from django.core.management import call_command
from django.utils.timezone import localdate

from tests.factories import QuestionFactory


def test_no_change():
    question = QuestionFactory.create()

    assert question.ranking == 10

    call_command("update_daily_ranking")

    question.refresh_from_db()

    assert question.ranking == 10


def test_change():
    # auto_add_now it is not overriden by factory boy
    old_date = localdate() - timedelta(days=3)

    question_1 = QuestionFactory.create(ranking=50)

    question_2 = QuestionFactory.create(ranking=40)
    question_2.created = old_date
    question_2.save()
    question_2.refresh_from_db()

    assert question_2.created < localdate()
    assert question_2.is_from_today

    question_3 = QuestionFactory.create(ranking=30)
    question_3.created = old_date
    question_3.save()

    assert question_1.ranking == 50
    assert question_2.ranking == 40
    assert question_3.ranking == 30

    call_command("update_daily_ranking")

    question_1.refresh_from_db()
    question_2.refresh_from_db()
    question_3.refresh_from_db()

    assert question_1.ranking == 50
    assert question_1.is_from_today

    assert question_2.ranking == 30
    assert not question_2.is_from_today

    assert question_3.ranking == 20
    assert not question_3.is_from_today
