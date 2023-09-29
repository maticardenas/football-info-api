from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_create_user_success(client: APIClient):
    # given
    url = reverse("user:user")
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
    }

    # when
    response = client.post(url, payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    created_user = get_user_model().objects.get(email=response.data["email"])
    assert created_user.check_password(payload["password"]) is True
    assert "password" not in response.data


def test_create_user_already_exists(client: APIClient, user_factory: get_user_model()):
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


def test_password_too_short(client: APIClient):
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


def test_get_users(client: APIClient, logged_in_admin_user: get_user_model()):
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


def test_get_users_no_admin(client: APIClient, logged_in_user: get_user_model()):
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


def test_retrieve_user_unauthorized(client: APIClient):
    # given
    url = reverse("user:me")

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_retrieve_user(client: APIClient, logged_in_user: get_user_model()):
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
    client: APIClient, logged_in_user: get_user_model()
):
    # given
    url = reverse("user:me")
    client.force_authenticate(user=logged_in_user)

    # when
    response = client.post(url)

    # then
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
