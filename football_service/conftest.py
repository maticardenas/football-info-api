from pathlib import Path
from typing import Callable

import pytest
from django.contrib.auth import get_user_model
from openapi_tester import SchemaTester
from utils.test_utils.test_client import FootTestClient

CURRENT_PATH = Path().absolute()


@pytest.fixture
def schema_tester_factory() -> Callable:
    def schema_tester(schema_file: Path) -> SchemaTester:
        return SchemaTester(schema_file_path=schema_file)

    return schema_tester


@pytest.fixture
def openapi_client_factory() -> Callable:
    def openapi_client(schema_tester: SchemaTester):
        from openapi_tester.clients import OpenAPIClient

        return OpenAPIClient(schema_tester=schema_tester)

    return openapi_client


@pytest.fixture
def client_factory():
    def client(schema_tester: SchemaTester = None):
        return FootTestClient(schema_tester=schema_tester)

    return client


@pytest.fixture
def user_factory(**params):
    def user(**params):
        return get_user_model().objects.create_user(**params)

    return user


@pytest.fixture
def user():
    return get_user_model().objects.create_user("test_user")


@pytest.fixture
def logged_in_admin_user(client):
    admin_user = get_user_model().objects.create_superuser(
        email="admin@example.com",
        password="password123",
    )
    client.force_login(admin_user)
    return admin_user


@pytest.fixture
def logged_in_user(client):
    user = get_user_model().objects.create_user(
        email="user@example.com",
        password="password123",
    )
    client.force_login(user)
    return user


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
