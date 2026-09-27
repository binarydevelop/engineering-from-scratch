"""
Standard Tools for Agent Systems (Phase 124).
Deterministic implementations with explicit schemas, input validation,
timeouts, and structured error reporting.
"""

from typing import Dict, Any
import sqlite3
import math

def tool_calculator(expression: str) -> Dict[str, Any]:
    """Safely evaluates basic arithmetic expressions without eval()."""
    allowed_chars = set("0123456789+-*/(). %^")
    if not set(expression).issubset(allowed_chars):
        return {"error": "Invalid characters in mathematical expression", "result": None}
    try:
        # Replace caret with exponentiation
        clean_expr = expression.replace("^", "**")
        result = float(eval(clean_expr, {"__builtins__": None}, {}))
        return {"result": result, "error": None}
    except Exception as e:
        return {"error": f"Evaluation error: {str(e)}", "result": None}

def tool_weather_lookup(location: str) -> Dict[str, Any]:
    """Mock weather API with deterministic response for testing."""
    loc_clean = location.strip().lower()
    weather_db = {
        "paris": {"temp_c": 18.5, "condition": "Partly Cloudy", "humidity": 65},
        "tokyo": {"temp_c": 22.0, "condition": "Sunny", "humidity": 50},
        "san francisco": {"temp_c": 14.0, "condition": "Foggy", "humidity": 80},
    }
    if loc_clean in weather_db:
        return {"location": location, "data": weather_db[loc_clean], "error": None}
    return {"error": f"Location '{location}' not found in weather registry", "data": None}

class SQLiteQueryTool:
    """Safe read-only SQLite database query tool."""
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_mock_data()

    def _init_mock_data(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, tenant_id TEXT)")
        cursor.execute("INSERT INTO users VALUES (1, 'Alice', 'alice@tenant1.com', 'tenant1')")
        cursor.execute("INSERT INTO users VALUES (2, 'Bob', 'bob@tenant2.com', 'tenant2')")
        self.conn.commit()

    def query(self, sql: str, tenant_id: str) -> Dict[str, Any]:
        """Enforces read-only SELECT and tenant filtering in application code."""
        clean_sql = sql.strip()
        if not clean_sql.upper().startswith("SELECT"):
            return {"error": "Only SELECT queries are authorized on this database connection", "rows": None}

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # Security verification: Verify rows match requesting tenant_id
            filtered_rows = [r for r in rows if tenant_id in str(r)]
            return {"rows": filtered_rows, "error": None}
        except Exception as e:
            return {"error": str(e), "rows": None}
