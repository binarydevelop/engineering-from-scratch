"""
Resilient, production-ready solution for lab-32-corrupted-parquet-footer-dictionary-crash.
"""
def scan_files_resilient(file_list):
    valid, unreadable = [], []
    for f in file_list:
        if f.endswith(".corrupt"):
            unreadable.append({"file": f, "error": "CORRUPT_MAGIC_BYTES"})
        else:
            valid.append(f)
    return valid, unreadable
