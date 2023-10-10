import json
from typing import TYPE_CHECKING, Callable
from unittest.mock import MagicMock

from django.core.handlers.wsgi import WSGIRequest
from openapi_tester import SchemaTester
from openapi_tester.clients import OpenAPIClient

if TYPE_CHECKING:
    from requests import Response


class FootTestClient(OpenAPIClient):
    def __init__(self, schema_tester: SchemaTester = None):
        super().__init__(schema_tester=schema_tester)
        self._openapi_validate = True if schema_tester else False

    @property
    def openapi_validate(self) -> bool:
        return self._openapi_validate

    @openapi_validate.setter
    def openapi_validate(self, value: bool) -> None:
        self._openapi_validate = value

    def json_support(function: Callable) -> Callable:
        def wrapped(self, *args, **kwargs):
            if "json" in kwargs:
                kwargs["data"] = json.dumps(kwargs["json"])
                kwargs["content_type"] = "application/json"
            return function(self, *args, **kwargs)

        return wrapped

    @json_support
    def post(self, *args, **kwargs) -> WSGIRequest:
        return super().post(*args, **kwargs)

    @json_support
    def put(self, *args, **kwargs) -> WSGIRequest:
        return super().put(*args, **kwargs)

    @json_support
    def patch(self, *args, **kwargs) -> WSGIRequest:
        return super().patch(*args, **kwargs)

    def request(self, **kwargs) -> "Response":  # type: ignore[override]
        if self.openapi_validate:
            return super().request(**kwargs)
        else:
            self.schema_tester = MagicMock()
            self.schema_tester.validate_response = MagicMock()
            return super().request(**kwargs)
