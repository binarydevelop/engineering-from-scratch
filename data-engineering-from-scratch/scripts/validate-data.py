#!/usr/bin/env python3
"""
Data Validation Utility for Data Engineering From Scratch
Validates datasets against basic schema contracts and invariant rules.
"""
import sys
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "datasets" / "raw"
CORRUPTED_DIR = BASE_DIR / "datasets" / "corrupted"

def validate_csv_table(path, pk_field, required_fields, expected_min_rows=1):
    if not path.exists():
        return False, f"File {path.name} does not exist"

    seen_pks = set()
    row_count = 0
    errors = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=1):
            row_count += 1
            pk = row.get(pk_field, "").strip()
            if not pk:
                errors.append(f"Row {row_num}: Missing primary key '{pk_field}'")
            elif pk in seen_pks:
                errors.append(f"Row {row_num}: Duplicate primary key '{pk}'")
            else:
                seen_pks.add(pk)

            for req in required_fields:
                val = row.get(req, "").strip()
                if not val:
                    errors.append(f"Row {row_num}: Required field '{req}' is null or empty")

    if row_count < expected_min_rows:
        errors.append(f"Expected at least {expected_min_rows} rows, got {row_count}")

    if errors:
        return False, f"{len(errors)} errors found (first 3): {errors[:3]}"
    return True, f"Valid ({row_count} rows, PK '{pk_field}' strictly unique)"

def main():
    print("=" * 60)
    print("  Data Engineering From Scratch - Dataset Validator")
    print("=" * 60)

    tables = [
        (RAW_DIR / "users.csv", "user_id", ["email", "full_name", "signup_date"]),
        (RAW_DIR / "products.csv", "product_id", ["sku", "category", "price"]),
        (RAW_DIR / "orders.csv", "order_id", ["user_id", "order_status", "total_amount", "created_at"]),
        (RAW_DIR / "order_items.csv", "item_id", ["order_id", "product_id", "quantity", "line_total"]),
        (RAW_DIR / "payments.csv", "payment_id", ["order_id", "amount", "payment_status"])
    ]

    all_passed = True
    print("\n--- Validating Production Raw Tables (Expect PASS) ---")
    for filepath, pk, reqs in tables:
        ok, msg = validate_csv_table(filepath, pk, reqs)
        status = "[PASS]" if ok else "[FAIL]"
        print(f"  {status} {filepath.name:<18} -> {msg}")
        if not ok:
            all_passed = False

    print("\n--- Validating Corrupted Dataset (Expect FAIL / Quality Catch) ---")
    corrupt_file = CORRUPTED_DIR / "corrupted_orders.csv"
    ok, msg = validate_csv_table(corrupt_file, "order_id", ["user_id", "order_status", "total_amount"])
    if not ok:
        print(f"  [EXPECTED CATCH] {corrupt_file.name} caught: {msg}")
    else:
        print(f"  [UNEXPECTED PASS] Corrupted file failed to trigger quality check!")
        all_passed = False

    print("=" * 60)
    if all_passed:
        print("All data contract checks passed successfully.")
        return 0
    else:
        print("Validation errors detected.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
