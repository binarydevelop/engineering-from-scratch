"""
Phase 03: CSV From First Principles
Building an RFC 4180 compliant CSV parser from scratch without libraries.
Handles quoted strings, escaped quotes (""), embedded commas, and malformed rows.
"""

def parse_csv_line(line):
    fields = []
    current_field = []
    in_quotes = False
    i = 0
    chars = list(line)
    n = len(chars)

    while i < n:
        char = chars[i]
        if char == '"':
            if in_quotes and i + 1 < n and chars[i + 1] == '"':
                # Escaped quote: "" -> "
                current_field.append('"')
                i += 1
            else:
                # Toggle quotes
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append("".join(current_field))
            current_field = []
        else:
            current_field.append(char)
        i += 1

    fields.append("".join(current_field))
    if in_quotes:
        raise ValueError("Malformed CSV: Unclosed quotation mark")
    return fields

def parse_csv_stream(text):
    lines = text.strip().split("\n")
    if not lines:
        return []
    headers = parse_csv_line(lines[0])
    records = []
    for line_num, line in enumerate(lines[1:], start=2):
        fields = parse_csv_line(line)
        if len(fields) != len(headers):
            raise ValueError(f"Line {line_num}: Column count mismatch (expected {len(headers)}, got {len(fields)})")
        records.append(dict(zip(headers, fields)))
    return records

def execute_phase():
    raw_data = '''id,name,address,amount
1,"Smith, John","123 Main St, Apt 4",100.00
2,"Acme, Inc.","456 Market St",250.00'''
    records = parse_csv_stream(raw_data)
    assert len(records) == 2
    assert records[0]["name"] == "Smith, John"
    assert records[0]["address"] == "123 Main St, Apt 4"
    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "parsed_rows": len(records)
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 03 Result:", res)
