"""
Broken implementation demonstrating the flaw in lab-21-lineage-graph-broken-dependency-gap.
"""
# Broken: Untracked ad-hoc intermediate table
def run_transform_broken(db):
    db["temp_untracked"] = db["raw"]
    db["mart"] = db["temp_untracked"]
