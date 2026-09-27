"""
Broken implementation demonstrating the flaw in lab-11-partial-write-missing-atomic-commit.
"""
def write_direct(target_dir, files):
    for f in files:
        # Writes directly to prod directory
        (target_dir / f).touch()
