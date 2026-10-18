"""The removal callback must never permit deleting a real inverter device."""
import ast
import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


@pytest.mark.parametrize("identifiers,entries,entities,allowed", [
    ({("sungrow", "")}, {"entry"}, [], True),
    ({("sungrow", "ABC")}, {"entry"}, [], False),
    ({("sungrow", "")}, {"entry"}, ["disabled_sensor"], False),
    ({("sungrow", "")}, {"entry", "other"}, [], False),
    (set(), {"entry"}, [], False),
])
def test_only_empty_legacy_device_can_be_removed(identifiers, entries, entities, allowed):
    path = Path(__file__).resolve().parents[1] / "custom_components/sungrow/__init__.py"
    tree = ast.parse(path.read_text())
    tree.body = [node for node in tree.body if isinstance(node, ast.AsyncFunctionDef)
                 and node.name == "async_remove_config_entry_device"]
    registry = SimpleNamespace(async_get=Mock(), async_entries_for_device=Mock(return_value=entities))
    namespace = dict(HomeAssistant=object, ConfigEntry=object, DOMAIN="sungrow",
                     dr=SimpleNamespace(DeviceEntry=object), er=registry)
    exec(compile(tree, str(path), "exec"), namespace)
    device = SimpleNamespace(id="device", identifiers=identifiers, config_entries=entries)
    assert asyncio.run(namespace["async_remove_config_entry_device"](
        object(), SimpleNamespace(entry_id="entry"), device)) == allowed
    if identifiers == {("sungrow", "")} and entries == {"entry"}:
        assert registry.async_entries_for_device.call_args.kwargs["include_disabled_entities"] is True
