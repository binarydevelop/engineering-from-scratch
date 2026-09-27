-- E-Commerce Dataset Seed
SET search_path TO ecommerce, public;

-- Categories (with hierarchical parent_id)
INSERT INTO categories (id, parent_id, name, slug) VALUES
(1, NULL, 'Electronics', 'electronics'),
(2, 1, 'Laptops & Computers', 'laptops-computers'),
(3, 1, 'Audio & Headphones', 'audio-headphones'),
(4, 1, 'Smartphones & Tablets', 'smartphones-tablets'),
(5, NULL, 'Home & Kitchen', 'home-kitchen'),
(6, 5, 'Coffee & Tea', 'coffee-tea'),
(7, 5, 'Cookware', 'cookware'),
(8, NULL, 'Books & Media', 'books-media');

SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));

-- Products
INSERT INTO products (id, category_id, name, sku, price, cost, is_active, created_at) VALUES
(1, 2, 'UltraBook Pro 15', 'TECH-LAP-001', 1299.99, 850.00, TRUE, '2025-10-01 10:00:00+00'),
(2, 2, 'Developer Workstation Mini', 'TECH-LAP-002', 899.50, 600.00, TRUE, '2025-10-05 11:30:00+00'),
(3, 3, 'Noise Cancelling Headphones X', 'AUDIO-NC-001', 249.99, 110.00, TRUE, '2025-11-01 09:00:00+00'),
(4, 3, 'Studio In-Ear Monitors', 'AUDIO-IEM-002', 129.00, 55.00, TRUE, '2025-11-15 14:20:00+00'),
(5, 4, 'Pro Phone 14', 'PHONE-PR-001', 999.00, 620.00, TRUE, '2025-12-01 08:00:00+00'),
(6, 4, 'Budget Smartphone Air', 'PHONE-BG-002', 299.99, 180.00, TRUE, '2025-12-10 12:00:00+00'),
(7, 6, 'Espresso Machine Maestro', 'HOME-ESP-001', 599.99, 340.00, TRUE, '2025-09-01 10:00:00+00'),
(8, 6, 'Precision Coffee Grinder', 'HOME-GRD-002', 149.50, 75.00, TRUE, '2025-09-15 16:45:00+00'),
(9, 7, 'Cast Iron Skillet 12-inch', 'HOME-PAN-003', 49.99, 20.00, TRUE, '2025-08-01 11:00:00+00'),
(10, 8, 'Designing Data-Intensive Applications', 'BOOK-DDIA-01', 45.00, 22.00, TRUE, '2025-07-01 09:00:00+00'),
(11, 8, 'Database Internals: A Deep Dive', 'BOOK-DBIN-02', 55.00, 28.00, TRUE, '2025-07-15 10:30:00+00'),
(12, 2, 'Discontinued Netbook 10', 'TECH-LAP-OLD', 199.99, 150.00, FALSE, '2024-01-01 00:00:00+00');

SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));

-- Inventory
INSERT INTO inventory (product_id, stock_quantity, reorder_level) VALUES
(1, 45, 10),
(2, 20, 5),
(3, 120, 25),
(4, 85, 20),
(5, 60, 15),
(6, 110, 30),
(7, 18, 5),
(8, 35, 10),
(9, 90, 20),
(10, 200, 50),
(11, 150, 40),
(12, 0, 5);

-- Customers (15 customers, including customers with no orders)
INSERT INTO customers (id, email, first_name, last_name, status, created_at) VALUES
(1, 'alice.smith@example.com', 'Alice', 'Smith', 'active', '2025-10-01 08:30:00+00'),
(2, 'bob.jones@example.com', 'Bob', 'Jones', 'active', '2025-10-15 09:45:00+00'),
(3, 'carol.davis@example.com', 'Carol', 'Davis', 'active', '2025-11-01 14:10:00+00'),
(4, 'david.wilson@example.com', 'David', 'Wilson', 'active', '2025-11-20 11:25:00+00'),
(5, 'eva.brown@example.com', 'Eva', 'Brown', 'active', '2025-12-05 16:50:00+00'),
(6, 'frank.miller@example.com', 'Frank', 'Miller', 'active', '2026-01-02 10:15:00+00'),
(7, 'grace.taylor@example.com', 'Grace', 'Taylor', 'active', '2026-01-10 13:40:00+00'),
(8, 'henry.clark@example.com', 'Henry', 'Clark', 'active', '2026-01-20 15:30:00+00'),
(9, 'isla.moore@example.com', 'Isla', 'Moore', 'active', '2026-02-01 09:00:00+00'),
(10, 'jack.white@example.com', 'Jack', 'White', 'suspended', '2026-02-05 11:10:00+00'),
(11, 'karen.hall@example.com', 'Karen', 'Hall', 'active', '2026-02-10 17:00:00+00'),
(12, 'leo.martin@example.com', 'Leo', 'Martin', 'active', '2026-02-15 12:30:00+00'),
(13, 'mia.thompson@example.com', 'Mia', 'Thompson', 'active', '2026-02-20 08:45:00+00'),
(14, 'noah.garcia@example.com', 'Noah', 'Garcia', 'active', '2026-03-01 14:00:00+00'),  -- Zero orders
(15, 'olivia.martinez@example.com', 'Olivia', 'Martinez', 'active', '2026-03-05 16:20:00+00'); -- Zero orders

SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));

-- Addresses
INSERT INTO addresses (id, customer_id, street, city, state, postal_code, country, is_default) VALUES
(1, 1, '123 Market St', 'San Francisco', 'CA', '94105', 'USA', TRUE),
(2, 2, '456 Elm St', 'Austin', 'TX', '78701', 'USA', TRUE),
(3, 3, '789 Broadway', 'New York', 'NY', '10003', 'USA', TRUE),
(4, 4, '321 Pine Rd', 'Seattle', 'WA', '98101', 'USA', TRUE),
(5, 5, '654 Maple Ave', 'Chicago', 'IL', '60601', 'USA', TRUE),
(6, 6, '987 Oak Dr', 'Denver', 'CO', '80202', 'USA', TRUE),
(7, 7, '234 Cedar St', 'San Francisco', 'CA', '94107', 'USA', TRUE),
(8, 8, '567 Birch Ln', 'Austin', 'TX', '78704', 'USA', TRUE),
(9, 9, '890 Walnut Blvd', 'Boston', 'MA', '02108', 'USA', TRUE),
(10, 10, '135 Spruce Way', 'Seattle', 'WA', '98104', 'USA', TRUE);

SELECT setval('addresses_id_seq', (SELECT MAX(id) FROM addresses));

-- Orders
INSERT INTO orders (id, customer_id, status, total_amount, shipping_address_id, order_date) VALUES
(1, 1, 'completed', 1549.98, 1, '2026-01-05 14:30:00+00'),
(2, 2, 'completed', 249.99, 2, '2026-01-10 16:15:00+00'),
(3, 3, 'completed', 749.49, 3, '2026-01-12 11:00:00+00'),
(4, 1, 'completed', 100.00, 1, '2026-01-20 09:20:00+00'),
(5, 4, 'completed', 999.00, 4, '2026-01-25 18:45:00+00'),
(6, 5, 'completed', 49.99, 5, '2026-02-01 10:10:00+00'),
(7, 6, 'completed', 1428.99, 6, '2026-02-05 13:00:00+00'),
(8, 7, 'completed', 378.99, 7, '2026-02-10 15:30:00+00'),
(9, 8, 'refunded', 299.99, 8, '2026-02-12 12:40:00+00'),
(10, 2, 'completed', 129.00, 2, '2026-02-18 17:15:00+00'),
(11, 9, 'completed', 899.50, 9, '2026-02-22 09:50:00+00'),
(12, 1, 'completed', 599.99, 1, '2026-02-28 14:05:00+00'),
(13, 3, 'completed', 1299.99, 3, '2026-03-01 11:30:00+00'),
(14, 5, 'cancelled', 249.99, 5, '2026-03-05 08:20:00+00'),
(15, 11, 'completed', 100.00, NULL, '2026-03-10 16:00:00+00'),
(16, 12, 'completed', 45.00, NULL, '2026-03-12 13:10:00+00'),
(17, 13, 'pending', 149.50, NULL, '2026-03-15 10:00:00+00');

SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));

-- Order Items
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 1299.99),
(2, 1, 3, 1, 249.99),
(3, 2, 3, 1, 249.99),
(4, 3, 7, 1, 599.99),
(5, 3, 8, 1, 149.50),
(6, 4, 10, 1, 45.00),
(7, 4, 11, 1, 55.00),
(8, 5, 5, 1, 999.00),
(9, 6, 9, 1, 49.99),
(10, 7, 1, 1, 1299.99),
(11, 7, 4, 1, 129.00),
(12, 8, 3, 1, 249.99),
(13, 8, 4, 1, 129.00),
(14, 9, 6, 1, 299.99),
(15, 10, 4, 1, 129.00),
(16, 11, 2, 1, 899.50),
(17, 12, 7, 1, 599.99),
(18, 13, 1, 1, 1299.99),
(19, 14, 3, 1, 249.99),
(20, 15, 10, 1, 45.00),
(21, 15, 11, 1, 55.00),
(22, 16, 10, 1, 45.00),
(23, 17, 8, 1, 149.50);

SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));

-- Payments
INSERT INTO payments (id, order_id, payment_method, amount, status, transaction_reference, created_at) VALUES
(1, 1, 'credit_card', 1549.98, 'completed', 'txn_cc_1001', '2026-01-05 14:31:00+00'),
(2, 2, 'paypal', 249.99, 'completed', 'txn_pp_1002', '2026-01-10 16:16:00+00'),
(3, 3, 'apple_pay', 749.49, 'completed', 'txn_ap_1003', '2026-01-12 11:01:00+00'),
(4, 4, 'credit_card', 100.00, 'completed', 'txn_cc_1004', '2026-01-20 09:21:00+00'),
(5, 5, 'credit_card', 999.00, 'completed', 'txn_cc_1005', '2026-01-25 18:46:00+00'),
(6, 6, 'apple_pay', 49.99, 'completed', 'txn_ap_1006', '2026-02-01 10:11:00+00'),
(7, 7, 'credit_card', 1428.99, 'completed', 'txn_cc_1007', '2026-02-05 13:01:00+00'),
(8, 8, 'paypal', 378.99, 'completed', 'txn_pp_1008', '2026-02-10 15:31:00+00'),
(9, 9, 'credit_card', 299.99, 'completed', 'txn_cc_1009', '2026-02-12 12:41:00+00'),
(10, 10, 'paypal', 129.00, 'completed', 'txn_pp_1010', '2026-02-18 17:16:00+00'),
(11, 11, 'credit_card', 899.50, 'completed', 'txn_cc_1011', '2026-02-22 09:51:00+00'),
(12, 12, 'apple_pay', 599.99, 'completed', 'txn_ap_1012', '2026-02-28 14:06:00+00'),
(13, 13, 'credit_card', 1299.99, 'completed', 'txn_cc_1013', '2026-03-01 11:31:00+00'),
(14, 15, 'credit_card', 100.00, 'completed', 'txn_cc_1015', '2026-03-10 16:01:00+00'),
(15, 16, 'paypal', 45.00, 'completed', 'txn_pp_1016', '2026-03-12 13:11:00+00');

SELECT setval('payments_id_seq', (SELECT MAX(id) FROM payments));

-- Refunds
INSERT INTO refunds (id, order_id, payment_id, amount, reason, created_at) VALUES
(1, 9, 9, 299.99, 'Customer requested return: Defective microphone unit', '2026-02-15 14:00:00+00');

SELECT setval('refunds_id_seq', (SELECT MAX(id) FROM refunds));
