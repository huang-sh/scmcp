from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
)
from typing import Any, get_origin, get_args
import json
from datetime import datetime

# Refer to https://github.dev/ckreiling/mcp-server-docker/tree/main/src/mcp_server_docker
class JSONParsingModel(BaseModel):
    """
    A base Pydantic model that attempts to parse JSON strings for non-primitive fields.
    If a string is provided for a field that expects a complex type (dict, list, or another model),
    it will attempt to parse it as JSON.

    Claude appears to not understand that a nested field shouldn't be a JSON-encoded string...
    But it does send valid JSON!
    """

    @field_validator("*", mode="before")
    @classmethod
    def _try_parse_json(cls, value: Any, info: ValidationInfo):
        if not isinstance(value, str):
            return value

        fields = cls.model_fields
        field_name = info.field_name

        if field_name not in fields:
            return value

        field = fields[field_name]
        field_type = field.annotation

        # Handle Optional/Union types
        origin = get_origin(field_type)
        if origin is not None:
            args = get_args(field_type)
            # Find the non-None type in case of Optional
            field_type = next(
                (arg for arg in args if arg is not type(None)), field_type
            )

        # Don't try to parse strings, numbers, or dates
        if field_type in (str, int, float, bool, datetime):
            return value

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value