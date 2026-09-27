def apply_scd2(dimension, natural_key, new_attrs, effective_date):
    for r in dimension:
        if r["natural_key"] == natural_key and r.get("is_current", True):
            r["is_current"] = False
            r["valid_to"] = effective_date
    dimension.append({
        "natural_key": natural_key,
        "is_current": True,
        "valid_from": effective_date,
        "valid_to": None,
        **new_attrs
    })
