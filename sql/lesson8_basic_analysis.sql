SELECT COUNT(*) AS total_orders
FROM orders;
SELECT MIN(order_purchase_timestamp) AS first_order
FROM orders;
SELECT MAX(order_purchase_timestamp) AS latest_order
FROM orders;
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
SELECT
AVG(order_delivered_customer_date - order_purchase_timestamp)
AS average_delivery_time
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;