from pytest import fixture
from django.test import Client
from .factories import UserFactory


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """This path is always for tests"""


@fixture
def user():
    return UserFactory()


@fixture
def client(user):
    client = Client()
    client.force_login(user)
    return client
