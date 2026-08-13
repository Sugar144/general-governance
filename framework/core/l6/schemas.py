"""Draft 2020-12 JSON Schema loading and stable validation."""

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .diagnostics import Diagnostic, ordered


def load_schema(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    return schema


def validate(instance: Any, schema: dict[str, Any], prefix: str = "$" ) -> list[Diagnostic]:
    result = []
    for error in Draft202012Validator(schema).iter_errors(instance):
        location = ".".join(str(part) for part in error.absolute_path)
        result.append(Diagnostic("SCHEMA_VALIDATION_FAILED", f"{prefix}.{location}".rstrip("."), error.message))
    return ordered(result)
