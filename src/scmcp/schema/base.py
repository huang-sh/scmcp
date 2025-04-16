from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
)
from typing import Any, get_origin, get_args, Union, Optional, Tuple, ClassVar
import json
from datetime import datetime


class JSONParsingModel(BaseModel):
    """
    # Refer to https://github.dev/ckreiling/mcp-server-docker/tree/main/src/mcp_server_docker
    """

    # Primitive types that don't need JSON parsing
    PRIMITIVE_TYPES: ClassVar[tuple] = (str, int, float, bool, datetime)

    @field_validator("*", mode="before")
    @classmethod
    def _try_parse_json(cls, value: Any, info: ValidationInfo) -> Any:
        # If not a string, return the original value
        if not isinstance(value, str):
            return value

        # Get field information
        field_name = info.field_name
        if not field_name or field_name not in cls.model_fields:
            return value


        field = cls.model_fields[field_name]
        field_type = field.annotation

        # Handle Optional and Union types
        origin = get_origin(field_type)
        if origin is not None:
            # For Optional[T] or Union[T, None], extract non-None type
            if origin is Union:
                args = get_args(field_type)
                # Find non-None types
                non_none_types = [arg for arg in args if arg is not type(None)]
                if non_none_types:
                    field_type = non_none_types[0]
        # If primitive type, don't parse JSON
        if field_type in cls.PRIMITIVE_TYPES:
            return value

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            # Return original value if parsing fails
            return value