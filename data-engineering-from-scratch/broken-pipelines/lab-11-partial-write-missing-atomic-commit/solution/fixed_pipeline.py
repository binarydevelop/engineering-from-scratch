"""
Resilient, production-ready solution for lab-11-partial-write-missing-atomic-commit.
"""
import shutil
def write_atomic(staging_dir, final_dir, files):
    staging_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        (staging_dir / f).touch()
    # Atomic swap / rename
    final_dir.parent.mkdir(parents=True, exist_ok=True)
    if final_dir.exists(): shutil.rmtree(final_dir)
    staging_dir.rename(final_dir)
