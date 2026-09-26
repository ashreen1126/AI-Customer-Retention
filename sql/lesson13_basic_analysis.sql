SELECT EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year FROM orders
LIMIT 10;
SELECT EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year,COUNT(*) AS total_orders
FROM orders GROUP BY order_year ORDER BY order_year;
SELECT EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month FROM orders
LIMIT 10;
SELECT EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month,
COUNT(*) AS total_orders FROM orders GROUP BY order_month ORDER BY order_month;
SELECT EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year,EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month,
COUNT(*) AS total_orders FROM orders
GROUP BY order_year, order_month ORDER BY order_year, order_month;
SELECT EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year FROM orders
LIMIT 10;
SELECT EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year,
COUNT(*) AS total_ordersFROM orders GROUP BY order_year ORDER BY order_year;
SELECT EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month,
COUNT(*) AS total_orders FROM orders GROUP BY order_month ORDER BY order_month;
SELECT EXTRACT(YEAR FROM order_purchase_timestamp) AS order_year,EXTRACT(MONTH FROM order_purchase_timestamp) AS order_month,
COUNT(*) AS total_orders FROM orders GROUP BY order_year, order_month ORDER BY order_year, order_month;