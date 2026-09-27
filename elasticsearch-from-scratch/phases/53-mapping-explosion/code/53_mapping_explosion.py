#!/usr/bin/env python3

def bad_modeling_dynamic_fields(user_ids):
    # Generates unique field per user
    fields = set()
    for uid in user_ids:
        fields.add(f"user_{uid}")
    return fields

def good_modeling_array(user_ids):
    # Fixed schema: 1 field
    return {"users_active": len(user_ids)}

if __name__ == "__main__":
    simulated_users = list(range(5000))
    bad_fields = bad_modeling_dynamic_fields(simulated_users)
    print("Anti-Pattern (Dynamic Field per ID):")
    print(f"  Total fields created in mapping: {len(bad_fields)} fields! (Triggers Mapping Explosion)")

    print("\nBest Practice (Fixed Array or Flattened):")
    print(f"  Total fields created in mapping: 1 field! (Stable)")
