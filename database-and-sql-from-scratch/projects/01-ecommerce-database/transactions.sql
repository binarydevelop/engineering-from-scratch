-- E-Commerce Checkout Transaction Flows with ACID Guarantees
SET search_path TO ecommerce, public;

-- Flow 1: Successful Checkout Transaction
-- Invariant: Atomically verify stock, deduct inventory, insert order, insert items, record payment.
BEGIN;

-- 1. Check stock with row lock to prevent race conditions (SELECT FOR UPDATE)
SELECT stock_quantity 
FROM inventory 
WHERE product_id = 1 
FOR UPDATE;

-- 2. Deduct inventory
UPDATE inventory 
SET stock_quantity = stock_quantity - 1, 
    updated_at = NOW() 
WHERE product_id = 1 AND stock_quantity >= 1;

-- 3. Create the order
INSERT INTO orders (id, customer_id, status, total_amount, shipping_address_id, order_date)
VALUES (101, 1, 'paid', 1299.99, 1, NOW());

-- 4. Insert order line item
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (101, 1, 1, 1299.99);

-- 5. Record successful payment
INSERT INTO payments (order_id, payment_method, amount, status, transaction_reference, created_at)
VALUES (101, 'credit_card', 1299.99, 'completed', 'txn_cc_success_101', NOW());

COMMIT;


-- Flow 2: Aborted Checkout (Simulated Inventory Depletion / Payment Rejection)
-- Demonstrates Atomicity: nothing is committed if a step fails.
BEGIN;

SELECT stock_quantity 
FROM inventory 
WHERE product_id = 12 
FOR UPDATE;

-- Product 12 has 0 stock!
-- Attempting to deduct stock triggers constraint violation or application abort:
-- We explicitly roll back to preserve initial database state.
ROLLBACK;
