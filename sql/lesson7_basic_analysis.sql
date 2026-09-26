SELECT COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(*) AS total_customers
FROM customers;

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;