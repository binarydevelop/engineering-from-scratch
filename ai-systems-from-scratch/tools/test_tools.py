import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from standard_tools import tool_calculator, tool_weather_lookup, SQLiteQueryTool
from sandboxed_executor import execute_sandboxed_code
from permission_manager import ToolPermissionManager, ActionType
from idempotent_tool_wrapper import IdempotencyStore

def test_calculator_and_weather():
    calc_res = tool_calculator("3 * (4 + 2) ^ 2")
    assert calc_res["result"] == 108.0

    bad_calc = tool_calculator("import os")
    assert bad_calc["error"] is not None

    w_res = tool_weather_lookup("Tokyo")
    assert w_res["data"]["temp_c"] == 22.0

def test_sqlite_tool():
    db = SQLiteQueryTool()
    res = db.query("SELECT * FROM users", tenant_id="tenant1")
    assert len(res["rows"]) == 1
    assert "Alice" in res["rows"][0][1]

    # Block non-SELECT
    bad_res = db.query("DROP TABLE users", tenant_id="tenant1")
    assert bad_res["error"] is not None

def test_sandboxed_executor():
    # Safe code
    safe_res = execute_sandboxed_code("total = sum([1, 2, 3, 4])\nprint(total)")
    assert safe_res["success"] is True
    assert safe_res["output"] == "10"

    # Malicious code attempt
    malicious = "import os\nos.system('ls')"
    bad_res = execute_sandboxed_code(malicious)
    assert bad_res["success"] is False
    assert "Security Policy Violation" in bad_res["error"]

def test_permissions_and_approval():
    pm = ToolPermissionManager()
    pm.register_tool("search_docs", ActionType.READ)
    pm.register_tool("refund_customer", ActionType.HIGH_STAKES)

    guest_check = pm.authorize("refund_customer", "guest")
    assert guest_check["authorized"] is False

    admin_check = pm.authorize("refund_customer", "admin")
    assert admin_check["authorized"] is True
    assert admin_check["requires_approval"] is True # High stakes requires approval!

def test_idempotency_wrapper():
    store = IdempotencyStore()
    call_count = 0

    def billing_call():
        nonlocal call_count
        call_count += 1
        return {"status": "CHARGED", "amount": 50.0}

    res1 = store.execute_idempotent("req_abc_123", billing_call)
    assert res1["_cached_replay"] is False
    assert call_count == 1

    # Retry with same idempotency key
    res2 = store.execute_idempotent("req_abc_123", billing_call)
    assert res2["_cached_replay"] is True
    assert call_count == 1 # Second call was prevented!
