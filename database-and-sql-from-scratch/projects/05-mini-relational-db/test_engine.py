"""
Tests for Mini Relational Database Engine using standard library unittest.
"""

import sys
import unittest
from pathlib import Path

# Add project path to sys.path
sys.path.insert(0, str(Path(__file__).parent))
from engine import Table, RelationalEngine


class TestMiniRelationalEngine(unittest.TestCase):

    def test_table_insert_and_pk_enforcement(self):
        customers = Table("customers", ["id", "email", "name"], "id")
        customers.insert({"id": 1, "email": "alice@example.com", "name": "Alice"})
        customers.insert({"id": 2, "email": "bob@example.com", "name": "Bob"})

        self.assertEqual(len(customers.scan()), 2)
        self.assertEqual(customers.lookup_pk(1)["name"], "Alice")
        self.assertIsNone(customers.lookup_pk(99))

        # Duplicate PK violation
        with self.assertRaises(ValueError):
            customers.insert({"id": 1, "email": "duplicate@example.com", "name": "Fake Alice"})

    def test_secondary_index(self):
        products = Table("products", ["id", "category_id", "name", "price"], "id")
        products.create_index("category_id")

        products.insert({"id": 101, "category_id": 1, "name": "Laptop", "price": 1000})
        products.insert({"id": 102, "category_id": 1, "name": "Mouse", "price": 25})
        products.insert({"id": 103, "category_id": 2, "name": "Coffee Maker", "price": 80})

        cat_1_prods = products.lookup_index("category_id", 1)
        self.assertEqual(len(cat_1_prods), 2)
        names = {p["name"] for p in cat_1_prods}
        self.assertEqual(names, {"Laptop", "Mouse"})

    def test_selection_and_projection(self):
        users = Table("users", ["id", "name", "age"], "id")
        users.insert({"id": 1, "name": "Alice", "age": 30})
        users.insert({"id": 2, "name": "Bob", "age": 17})
        users.insert({"id": 3, "name": "Carol", "age": 25})

        # Selection: WHERE age >= 18
        adults = RelationalEngine.select(users.scan(), lambda u: u["age"] >= 18)
        self.assertEqual(len(adults), 2)

        # Projection: SELECT id, name
        projected = RelationalEngine.project(adults, ["id", "name"])
        self.assertEqual(projected, [
            {"id": 1, "name": "Alice"},
            {"id": 3, "name": "Carol"}
        ])

    def test_joins(self):
        users = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ]
        orders = [
            {"order_id": 101, "user_id": 1, "amount": 50},
            {"order_id": 102, "user_id": 1, "amount": 75},
            {"order_id": 103, "user_id": 2, "amount": 200},
            {"order_id": 104, "user_id": 4, "amount": 999}
        ]

        # Nested Loop Join
        nl_res = RelationalEngine.nested_loop_join(orders, users, "user_id", "id")
        self.assertEqual(len(nl_res), 3)

        # Hash Join
        hj_res = RelationalEngine.hash_join(orders, users, "user_id", "id")
        self.assertEqual(len(hj_res), 3)
        self.assertEqual({r["right_name"] for r in hj_res}, {"Alice", "Bob"})


if __name__ == "__main__":
    unittest.main()
