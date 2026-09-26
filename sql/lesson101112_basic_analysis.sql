SELECT customer_city,customer_state FROM customers ORDER BY customer_city;
SELECT customer_city,customer_state FROM customers ORDER BY customer_city ASC
LIMIT 10;
SELECT order_id,order_purchase_timestamp FROM orders ORDER BY order_purchase_timestamp DESC
LIMIT 10;
SELECT * FROM orders
LIMIT 5;
SELECT * FROM orders
LIMIT 10
OFFSET 10;
SELECT customers.customer_city,COUNT(*) AS total_orders FROM customers INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_city
ORDER BY total_orders DESC
LIMIT 10;
SELECT order_id,order_purchase_timestamp FROM orders ORDER BY order_purchase_timestamp ASC
LIMIT 10;
SELECT order_id,order_purchase_timestamp FROM orders
ORDER BY order_purchase_timestamp DESC
LIMIT 10;
SELECT customer_city,customer_state FROM customers ORDER BY customer_city ASC
LIMIT 10;