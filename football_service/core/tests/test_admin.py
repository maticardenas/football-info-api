from core.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_users_list(client: APIClient, logged_in_admin_user: User):
    # given
    url = reverse("admin:core_user_changelist")

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert logged_in_admin_user.email in str(response.content)


def test_edit_admin_user_page(client: APIClient, logged_in_admin_user: User):
    # given
    url = reverse("admin:core_user_change", args=[logged_in_admin_user.id])

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert logged_in_admin_user.email in str(response.content)


def test_create_user_page(client: APIClient, logged_in_admin_user: User):
    # given
    url = reverse("admin:core_user_add")

    # when
    response = client.get(url)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert logged_in_admin_user.email in str(response.content)
