from pathlib import Path
from typing import Callable

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from openapi_tester.clients import OpenAPIClient
from rest_framework import status

TESTS_PATH = Path(__file__).parent.absolute()


@pytest.fixture
def users_api_schema() -> Path:
    return TESTS_PATH.parent.parent / "schemas" / "user" / "openapi.yaml"


@pytest.fixture
def client(
    schema_tester_factory: Callable,
    client_factory: Callable,
    users_api_schema: Path,
) -> OpenAPIClient:
    schema_tester = schema_tester_factory(users_api_schema)
    return client_factory(schema_tester)


def test_create_user_success(client: OpenAPIClient):
    # given
    url = reverse("user:user")
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
    }

    # when
    response = client.post(url, json=payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    created_user = get_user_model().objects.get(email=response.data["email"])
    assert created_user.check_password(payload["password"]) is True
    assert "password" not in response.data


def test_create_user_already_exists(
    client: OpenAPIClient, user_factory: get_user_model()
):
    # given
    url = reverse("user:user")
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
    }
    user_factory(**payload)

    # when
    response = client.post(url, payload)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" not in response.data


def test_password_too_short(client: OpenAPIClient):
    # given
    url = reverse("user:user")
    payload = {
        "email": "test@example.com",
        "password": "pw",
        "name": "Test User",
    }

    # when
    response = client.post(url, payload)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
    assert user_exists is False


def test_get_users(client: OpenAPIClient, logged_in_admin_user: get_user_model()):
    # given
    url = reverse("user:user")
    get_user_model().objects.create_user(
        email="another_no_admin_user@example.com",
        password="password123",
        name="Another No Admin User",
    )

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["email"] == logged_in_admin_user.email
    assert response.data[1]["email"] == "another_no_admin_user@example.com"


def test_get_users_no_admin(client: OpenAPIClient, logged_in_user: get_user_model()):
    # given
    url = reverse("user:user")
    get_user_model().objects.create_user(
        email="another_no_admin_user@example.com",
        password="password123",
        name="Another No Admin User",
    )

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["email"] == logged_in_user.email


def test_retrieve_user_unauthorized(client: OpenAPIClient):
    # given
    url = reverse("user:me")

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_retrieve_user(client: OpenAPIClient, logged_in_user: get_user_model()):
    # given
    url = reverse("user:me")
    client.force_authenticate(user=logged_in_user)

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == logged_in_user.email
    assert response.data["name"] == logged_in_user.name


def test_retrieve_user_method_not_allowed(
    client: OpenAPIClient, logged_in_user: get_user_model()
):
    # given
    url = reverse("user:me")
    client.force_authenticate(user=logged_in_user)
    client.openapi_validate = False

    # when
    response = client.post(url)

    # then
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
