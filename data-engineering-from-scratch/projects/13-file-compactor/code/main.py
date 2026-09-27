def compact_records(record_chunks):
    merged = []
    for chunk in record_chunks:
        merged.extend(chunk)
    return merged
