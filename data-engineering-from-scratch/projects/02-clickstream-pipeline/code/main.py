import json
from collections import defaultdict

def compute_funnel(events):
    funnel_stages = ["page_view", "add_to_cart", "checkout", "purchase"]
    user_stages = defaultdict(set)
    for e in events:
        user_stages[e["user_id"]].add(e["action"])
    
    stage_counts = {s: 0 for s in funnel_stages}
    for user, actions in user_stages.items():
        for s in funnel_stages:
            if s in actions:
                stage_counts[s] += 1
    return stage_counts
