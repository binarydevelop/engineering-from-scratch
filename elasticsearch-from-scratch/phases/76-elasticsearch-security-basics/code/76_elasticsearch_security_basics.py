#!/usr/bin/env python3

def check_permission(user_roles, role_definitions, index_name, action):
    # Action: "read" or "write"
    for r in user_roles:
        privs = role_definitions.get(r, {}).get("indices", {})
        for pattern, allowed_actions in privs.items():
            if pattern == "*" or pattern in index_name:
                if action in allowed_actions:
                    return True
    return False

if __name__ == "__main__":
    roles = {
        "analyst": {"indices": {"products_*": ["read"]}},
        "admin": {"indices": {"*": ["read", "write"]}}
    }
    print("Testing RBAC Security Rules:")
    print("  User 'alice' (analyst) reading 'products_v1' ->", check_permission(["analyst"], roles, "products_v1", "read"))
    print("  User 'alice' (analyst) writing to 'products_v1' ->", check_permission(["analyst"], roles, "products_v1", "write"))
    print("  User 'bob' (admin) writing to 'products_v1'     ->", check_permission(["admin"], roles, "products_v1", "write"))
