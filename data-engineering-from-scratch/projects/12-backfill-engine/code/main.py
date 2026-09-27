def backfill_partition(storage, date_str, new_records):
    storage[:] = [r for r in storage if r.get("date") != date_str]
    storage.extend(new_records)
    return len(storage)
