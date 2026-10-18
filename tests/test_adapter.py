"""Check coordinator failures and monitor-only register selection offline."""
import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import yaml

from test_reader import inverter

ROOT = Path(__file__).resolve().parents[1]


def adapter_namespace():
    path = ROOT / "custom_components/sungrow/inverter.py"
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    namespace = dict(pathlib=__import__("pathlib"), yaml=yaml,
                     __file__=str(path), SungrowInverter=object,
                     Tuple=__import__("typing").Tuple, UpdateFailed=RuntimeError,
                     pformat=repr, logger=Mock())
    exec(compile(tree, str(path), "exec"), namespace)
    return namespace


@pytest.mark.parametrize("connected,scraped", [(False, True), (True, False)])
def test_coordinator_rejects_failed_poll_even_with_old_data(connected, scraped):
    namespace = adapter_namespace()
    inv = SimpleNamespace(connect=Mock(return_value=connected), scrape=Mock(return_value=scraped),
                          last_register_read_failure="offline", latest_scrape={"old": 1})
    with pytest.raises(RuntimeError, match="offline"):
        namespace["data_updater"](inv)()


@pytest.mark.parametrize("smart_meter", [False, True])
def test_adapter_only_polls_monitoring_registers(smart_meter):
    namespace = adapter_namespace()
    inv = inverter()
    inv.inverter_config["smart_meter"] = smart_meter
    inv.checkConnection = Mock(return_value=True)
    namespace["SungrowInverter"] = Mock(return_value=inv)
    namespace["create_inverter"]({"smart_meter": smart_meter})()
    assert all(r["type"] == "read" for r in inv.registers)
    names = {r["name"] for r in inv.registers}
    assert ("meter_power" in names) == smart_meter
    if not smart_meter:
        assert not {"export_power", "power_meter"} & names
