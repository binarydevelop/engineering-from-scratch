#!/usr/bin/env python3

def evaluate_ilm(index_age_days, size_gb):
    if index_age_days >= 90:
        return "DELETE", "Delete index permanently"
    elif index_age_days >= 30:
        return "COLD", "Move to cold tier, freeze segments"
    elif index_age_days >= 7 or size_gb >= 50:
        return "WARM", "Rollover to new index, force-merge to 1 segment, move to warm tier"
    return "HOT", "Active write tier"

if __name__ == "__main__":
    test_cases = [(2, 20), (5, 55), (14, 40), (45, 30), (100, 30)]
    print("ILM Phase Transitions:")
    for age, size in test_cases:
        phase, action = evaluate_ilm(age, size)
        print(f"  Age: {age:3d}d, Size: {size:2d}GB ──► Phase: [{phase:6s}] - {action}")
