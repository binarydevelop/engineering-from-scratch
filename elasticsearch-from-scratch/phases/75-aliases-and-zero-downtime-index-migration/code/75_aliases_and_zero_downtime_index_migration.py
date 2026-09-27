#!/usr/bin/env python3

class AliasRouter:
    def __init__(self):
        self.aliases = {} # alias_name -> physical_index

    def set_alias(self, alias_name, physical_index):
        self.aliases[alias_name] = physical_index

    def atomic_swap(self, alias_name, old_index, new_index):
        if self.aliases.get(alias_name) == old_index:
            self.aliases[alias_name] = new_index
            return True
        return False

    def route_request(self, target):
        return self.aliases.get(target, target)

if __name__ == "__main__":
    router = AliasRouter()
    router.set_alias("products", "products_v1")
    print("Initial routing for 'products':", router.route_request("products"))

    print("\nReindexing products_v2 complete. Performing atomic swap...")
    success = router.atomic_swap("products", "products_v1", "products_v2")
    print(f"Swap succeeded: {success}")
    print("Routing for 'products' after swap:", router.route_request("products"))
