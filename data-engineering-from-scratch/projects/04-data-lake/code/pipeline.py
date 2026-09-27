from pathlib import Path

def stage_lake_partition(lake_root, zone, date_str, filename, content):
    target_dir = Path(lake_root) / zone / f"date={date_str}"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / filename
    target_file.write_text(content)
    return target_file
