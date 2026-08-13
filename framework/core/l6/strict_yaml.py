"""Strict UTF-8 YAML loading with duplicate mapping-key rejection."""

from pathlib import Path
from typing import Any

import yaml


class StrictYAMLError(ValueError):
    pass


class StrictLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise StrictYAMLError(f"unhashable mapping key at line {key_node.start_mark.line + 1}") from exc
        if duplicate:
            raise StrictYAMLError(
                f"duplicate mapping key {key!r} at line {key_node.start_mark.line + 1}"
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def loads(text: str, source: str = "<string>") -> Any:
    try:
        return yaml.load(text, Loader=StrictLoader)
    except (yaml.YAMLError, StrictYAMLError) as exc:
        raise StrictYAMLError(f"{source}: {exc}") from exc


def load_bytes(data: bytes, source: str = "<bytes>") -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StrictYAMLError(f"{source}: invalid UTF-8") from exc
    return loads(text, source)


def load(path: str | Path) -> Any:
    source = Path(path)
    try:
        data = source.read_bytes()
    except OSError as exc:
        raise StrictYAMLError(f"{source}: {exc}") from exc
    return load_bytes(data, str(source))
