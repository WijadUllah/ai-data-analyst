
-- 1. Add customers
INSERT INTO customers (customer_name, city)
VALUES
    ('Ali Khan', 'Peshawar'),
    ('Sara Ahmed', 'Islamabad'),
    ('Usman Malik', 'Mardan'),
    ('Ayesha Noor', 'Lahore'),
    ('Hamza Shah', 'Peshawar');

-- 2. Add products
INSERT INTO products (product_name, category, unit_price, stock_quantity)
VALUES
    ('Laptop', 'Electronics', 120000, 10),
    ('Smartphone', 'Electronics', 80000, 20),
    ('Headphones', 'Accessories', 5000, 50),
    ('Keyboard', 'Accessories', 3000, 30),
    ('Monitor', 'Electronics', 35000, 15);

-- 3. Add orders
INSERT INTO orders (customer_id, order_date, status)
VALUES
    (1, '2026-09-05', 'completed'),
    (2, '2026-09-10', 'completed'),
    (3, '2026-09-15', 'completed'),
    (1, '2026-10-02', 'completed'),
    (4, '2026-10-05', 'completed'),
    (5, '2026-10-08', 'cancelled');

-- 4. Add the products included in each order
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
    (1, 1, 1, 120000),
    (1, 3, 2, 5000),
    (2, 2, 1, 80000),
    (2, 4, 2, 3000),
    (3, 3, 3, 5000),
    (3, 5, 1, 35000),
    (4, 2, 2, 80000),
    (4, 3, 1, 5000),
    (5, 1, 1, 120000),
    (5, 5, 2, 35000),
    (6, 1, 1, 120000);
