import pytest
from graphene_django.utils.testing import graphql_query


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


@pytest.fixture
def staff_query(client, django_user_model):
    def func(*args, **kwargs):
        django_user_model.objects.create_user(email='admin@test.pl', password='qwerty', is_staff=True)
        client.login(email='admin@test.pl', password='qwerty')
        return graphql_query(*args, **kwargs, client=client)

    return func


