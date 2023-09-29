from django.urls import reverse
from rest_framework import status


def test_create_token_for_user(user_factory, client):
    # given
    token_url = reverse("user:token")
    payload = {
        "email": "test@example.com",
        "password": "password123",
    }
    user_factory(**{**payload, "name": "Test User"})

    # when
    response = client.post(token_url, payload)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert isinstance(response.data["token"], str)


def test_create_token_invalid_credentials(user_factory, client):
    # given
    token_url = reverse("user:token")
    payload = {
        "email": "test@example.com",
        "password": "password123",
    }
    user_factory(**{**payload, "name": "Test User"})
    payload["password"] = "wrong_password"

    # when
    response = client.post(token_url, payload)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "token" not in response.data


def test_create_token_no_user(user_factory, client):
    # given
    token_url = reverse("user:token")
    payload = {
        "email": "test@example.com",
        "password": "password123",
    }

    # when
    response = client.post(token_url, payload)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "token" not in response.data


def test_create_token_missing_field(client):
    # given
    token_url = reverse("user:token")
    payload = {
        "email": "test@example.com",
    }

    # when
    response = client.post(token_url, payload)

    # then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
