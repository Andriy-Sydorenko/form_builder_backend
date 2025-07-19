import re
from typing import Any

from pydantic import BaseModel, field_validator, model_validator

from app.constants import EMAIL_PATTERN


class BaseValidatedModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def check_empty_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(data, dict):
            return data

        for field_name, value in data.items():
            if isinstance(value, str) and value.strip() == "":
                raise ValueError(f"{field_name} cannot be empty or contain only whitespace")
        return data

    @field_validator("*")
    @classmethod
    def validate_email_fields(cls, v: Any, info: Any) -> Any:
        if "email" in info.field_name.lower() and isinstance(v, str) and not re.match(EMAIL_PATTERN, v):
            raise ValueError(f"Invalid email format: {v}")
        return v
