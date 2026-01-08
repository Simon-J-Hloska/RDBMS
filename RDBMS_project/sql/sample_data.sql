USE `orders_management`;

INSERT INTO customers (customer_id, first_name, last_name, email, phone, created_at) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '+420111222333', NOW()),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '+420444555666', NOW()),
(3, 'Alice', 'Brown', 'alice.brown@example.com', '+420777888999', NOW());

INSERT INTO products (product_id, name, description, price, stock_quantity, created_at) VALUES
(1, 'Laptop', '15-inch business laptop', 1200.00, 10, NOW()),
(2, 'Mouse', 'Wireless optical mouse', 25.50, 100, NOW()),
(3, 'Keyboard', 'Mechanical keyboard', 89.99, 50, NOW()),
(4, 'Monitor', '27-inch 4K display', 399.00, 20, NOW());

INSERT INTO orders (order_id, customer_id, order_date, status, total_amount) VALUES
(1, 1, NOW(), 'paid', 1250.50),
(2, 2, NOW(), 'pending', 89.99),
(3, 3, NOW(), 'paid', 399.00);

INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 1200.00, 1200.00),
(1, 2, 2, 25.25, 50.50),
(2, 3, 1, 89.99, 89.99),
(3, 4, 1, 399.00, 399.00);

INSERT INTO payments (order_id, payment_date, amount, payment_method, status) VALUES
(1, NOW(), 1250.50, 'CARD', 'COMPLETED'),
(3, NOW(), 399.00, 'BANK_TRANSFER', 'COMPLETED');
