import pytest
from django.contrib.auth import get_user_model


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def test_create_user_with_email_successful():
    # given
    email = "test@example.com"
    password = "Testpass123"

    # when
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
    )

    # then
    assert user.email == email
    assert user.check_password(password) is True


@pytest.mark.parametrize(
    "email, expected_normalized_email",
    [
        ("test1@EXAMPLE.com", "test1@example.com"),
        ("Test2@Example.com", "Test2@example.com"),
        ("TEST3@EXAMPLE.com", "TEST3@example.com"),
        ("test4@example.com", "test4@example.com"),
    ],
)
def test_create_user_with_normalized_email(email: str, expected_normalized_email: str):
    # given - when
    user = get_user_model().objects.create_user(email=email, password="Testpass123")

    # then
    assert user.email == expected_normalized_email


def test_create_user_with_normalized_email_fails():
    # given - when - then
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(email=None, password="Testpass123")


def test_create_superuser_successful():
    # given - when
    user = get_user_model().objects.create_superuser(
        email="test@example.com",
        password="Testpass123",
    )

    # then
    assert user.is_superuser is True
    assert user.is_staff is True
