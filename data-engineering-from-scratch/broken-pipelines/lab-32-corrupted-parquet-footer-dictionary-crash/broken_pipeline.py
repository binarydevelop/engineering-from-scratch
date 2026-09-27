"""
Broken implementation demonstrating the flaw in lab-32-corrupted-parquet-footer-dictionary-crash.
"""
def scan_files_broken(file_list):
    for f in file_list:
        if f.endswith(".corrupt"):
            raise ValueError("Invalid Parquet magic bytes")
