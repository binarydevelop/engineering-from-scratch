#!/usr/bin/env python3
"""
Lightweight Query Grader for Database and SQL from Scratch.

Compares a learner's query or exercise against the canonical reference solution.
Handles:
  - Execution via PostgreSQL (psycopg driver or docker exec psql fallback)
  - Column matching (names & count)
  - Row counts
  - Ordered vs Unordered result comparison
  - Numeric floating-point tolerance
  - NULL equivalence
"""

import sys
import os
import re
import argparse
import subprocess
import json
from pathlib import Path
from decimal import Decimal

# Try importing tabulate or rich, fallback gracefully
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

try:
    import psycopg
    HAS_PSYCOPG = True
except ImportError:
    try:
        import psycopg2 as psycopg
        HAS_PSYCOPG = True
    except ImportError:
        HAS_PSYCOPG = False


def get_db_connection_params():
    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "dbname": os.getenv("PGDATABASE", "sqllab"),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", "postgres"),
    }


def execute_query(sql: str):
    """
    Executes a query and returns (columns, rows, error_message).
    Uses psycopg if available, otherwise shells out to docker exec psql.
    """
    params = get_db_connection_params()
    
    # 1. Try psycopg
    if HAS_PSYCOPG:
        try:
            conn = psycopg.connect(
                host=params["host"],
                port=params["port"],
                dbname=params["dbname"],
                user=params["user"],
                password=params["password"],
                connect_timeout=3
            )
            with conn.cursor() as cur:
                # Set search path to all common schemas
                cur.execute("SET search_path TO ecommerce, social, saas, banking, analytics, public;")
                cur.execute(sql)
                if cur.description is None:
                    return [], [], None
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                # Normalize decimals to float / string for clean comparison
                norm_rows = []
                for r in rows:
                    norm_row = []
                    for val in r:
                        if isinstance(val, Decimal):
                            norm_row.append(float(val))
                        else:
                            norm_row.append(val)
                    norm_rows.append(tuple(norm_row))
                return columns, norm_rows, None
        except Exception as e:
            return None, None, str(e)

    # 2. Fallback to docker exec psql JSON output
    docker_cmd = [
        "docker", "exec", "-i", "database-sql-scratch-db",
        "psql", "-U", params["user"], "-d", params["dbname"],
        "-c", f"SET search_path TO ecommerce, social, saas, banking, analytics, public; {sql}",
        "-A", "-F", "\t"
    ]
    try:
        res = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=10)
        if res.returncode != 0:
            return None, None, res.stderr.strip()
        lines = [line for line in res.stdout.strip().split("\n") if line and not line.startswith("SET")]
        if not lines:
            return [], [], None
        columns = lines[0].split("\t")
        rows = [tuple(line.split("\t")) for line in lines[1:-1] if not line.endswith("rows)")]
        return columns, rows, None
    except Exception as e:
        return None, None, f"Execution failed: {e}"


def extract_sql_from_file(file_path: Path) -> str:
    """Extracts SQL query from .sql or .md markdown fenced block."""
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix == ".sql":
        return text.strip()
    
    # Check for ```sql ... ``` block
    matches = re.findall(r"```sql(.*?)```", text, re.DOTALL)
    if matches:
        return matches[-1].strip()
    return text.strip()


def normalize_value(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return round(float(val), 4)
    return str(val).strip()


def compare_results(learner_cols, learner_rows, ref_cols, ref_rows, requires_order=False):
    """
    Compares learner results with reference results.
    Returns (is_match, reason, details).
    """
    if len(learner_cols) != len(ref_cols):
        return False, f"Column count mismatch: Expected {len(ref_cols)} columns, got {len(learner_cols)}", None
    
    if len(learner_rows) != len(ref_rows):
        return False, f"Row count mismatch: Expected {len(ref_rows)} rows, got {len(learner_rows)}", None

    norm_ref = [[normalize_value(v) for v in row] for row in ref_rows]
    norm_learner = [[normalize_value(v) for v in row] for row in learner_rows]

    if requires_order:
        for idx, (l_row, r_row) in enumerate(zip(norm_learner, norm_ref)):
            if l_row != r_row:
                return False, f"Row mismatch at row index {idx}:\n  Expected: {r_row}\n  Received: {l_row}", None
    else:
        # Sort both for multiset equivalence comparison
        try:
            sorted_ref = sorted(norm_ref, key=lambda r: tuple(str(x) for x in r))
            sorted_learner = sorted(norm_learner, key=lambda r: tuple(str(x) for x in r))
            if sorted_learner != sorted_ref:
                return False, "Result set contents do not match reference records (unordered comparison).", None
        except Exception as e:
            return False, f"Comparison error: {e}", None

    return True, "SUCCESS: Result set matches reference solution perfectly!", None


def grade_single(query_path: str, verbose=True):
    path = Path(query_path)
    if not path.exists():
        print(f"[-] Error: File not found: {query_path}")
        return False

    learner_sql = extract_sql_from_file(path)

    # Determine reference solution path
    # If path is already inside solutions/, we compare it against itself or run verification
    root = Path(__file__).resolve().parent.parent
    abs_path = path.resolve()
    rel_path = abs_path.relative_to(root)

    ref_path = None
    if "solutions" in rel_path.parts:
        ref_path = abs_path
    elif "drills" in rel_path.parts:
        drill_subpath = abs_path.relative_to(root / "drills")
        ref_path = root / "solutions" / "drills" / drill_subpath.with_suffix(".sql")
    elif "exercises" in rel_path.parts:
        ex_subpath = abs_path.relative_to(root / "exercises")
        ref_path = root / "solutions" / ex_subpath.with_suffix(".sql")

    if ref_path and ref_path.exists() and ref_path != path:
        ref_sql = extract_sql_from_file(ref_path)
    else:
        ref_sql = learner_sql

    requires_order = "ORDER BY" in learner_sql.upper() or "ORDER BY" in ref_sql.upper()

    if verbose:
        print(f"\nEvaluating: {path.name}")
        print(f"Target:     {path}")
        if ref_path and ref_path != path:
            print(f"Reference:  {ref_path}")
        print("-" * 60)

    # Execute learner query
    l_cols, l_rows, l_err = execute_query(learner_sql)
    if l_err:
        print(f"[-] Execution Error in query:\n{l_err}")
        return False

    # Execute reference query
    r_cols, r_rows, r_err = execute_query(ref_sql)
    if r_err:
        print(f"[-] Reference Execution Error:\n{r_err}")
        return False

    matched, msg, _ = compare_results(l_cols, l_rows, r_cols, r_rows, requires_order)

    if matched:
        print(f"[+] PASS: {msg}")
        print(f"    Returned {len(l_rows)} rows x {len(l_cols)} columns.")
        if verbose and l_rows and HAS_TABULATE:
            sample = l_rows[:5]
            print("\nSample Output (First 5 rows):")
            print(tabulate(sample, headers=l_cols, tablefmt="psql"))
        return True
    else:
        print(f"[-] FAIL: {msg}")
        if verbose and HAS_TABULATE:
            print("\nExpected First 3 rows:")
            print(tabulate(r_rows[:3], headers=r_cols, tablefmt="psql"))
            print("\nActual Received First 3 rows:")
            print(tabulate(l_rows[:3], headers=l_cols, tablefmt="psql"))
        return False


def main():
    parser = argparse.ArgumentParser(description="Query Verification Grader")
    parser.add_argument("query", nargs="?", help="Path to .sql or .md file to grade")
    parser.add_argument("--all-drills", action="store_true", help="Grade all drills against solutions")
    parser.add_argument("--all-exercises", action="store_true", help="Grade all exercises against solutions")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent

    if args.all_drills:
        print("==> Grading all drills...")
        solutions = sorted((root / "solutions" / "drills").rglob("*.sql"))
        if not solutions:
            print("No drill solutions found yet.")
            return
        passed = 0
        for sol in solutions:
            if grade_single(str(sol), verbose=False):
                passed += 1
                print(f"  [PASS] {sol.name}")
            else:
                print(f"  [FAIL] {sol.name}")
        print(f"\nSummary: {passed}/{len(solutions)} drills passed.")
        sys.exit(0 if passed == len(solutions) else 1)

    if args.query:
        success = grade_single(args.query, verbose=True)
        sys.exit(0 if success else 1)

    parser.print_help()


if __name__ == "__main__":
    main()
