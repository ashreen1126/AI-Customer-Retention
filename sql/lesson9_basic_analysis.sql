SELECT * FROM orders
WHERE order_status = 'delivered';
SELECT COUNT(*) AS delivered_orders FROM orders WHERE order_status = 'delivered';
SELECT * FROM orders WHERE order_status = 'delivered' AND order_purchase_timestamp >= '2018-01-01'
LIMIT 10;
SELECT * FROM orders WHERE order_status = 'delivered' OR order_status = 'shipped'
LIMIT 10;
SELECT * FROM orders WHERE order_purchase_timestamp BETWEEN '2018-01-01' AND '2018-12-31'
LIMIT 10;
SELECT * FROM orders WHERE order_status IN ('delivered','shipped','processing')
LIMIT 10;
SELECT COUNT(*) AS delivered_orders FROM orders WHERE order_status = 'delivered';
SELECT COUNT(*) AS cancelled_orders FROM orders WHERE order_status = 'canceled';
SELECT customer_city FROM customers WHERE customer_city LIKE 'sao%'
LIMIT 10;
SELECT COUNT(*) AS orders_2018 FROM orders WHERE order_purchase_timestamp BETWEEN '2018-01-01' AND '2018-12-31';