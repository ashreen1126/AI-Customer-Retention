-- LESSON 14: PAYMENT & REVENUE ANALYSIS

-- 1. Count payment records
SELECT COUNT(*) AS total_payment_records
FROM order_payments;


-- 2. View payment data
SELECT *
FROM order_payments
LIMIT 10;


-- 3. Payment methods
SELECT
    payment_type,
    COUNT(*) AS total_payments
FROM order_payments
GROUP BY payment_type
ORDER BY total_payments DESC;


-- 4. Total payment value
SELECT
    SUM(payment_value) AS total_payment_value
FROM order_payments;


-- 5. Average payment
SELECT
    AVG(payment_value) AS average_payment
FROM order_payments;


-- 6. Payment value by method
SELECT
    payment_type,
    SUM(payment_value) AS total_payment_value
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- 7. Average installments
SELECT
    AVG(payment_installments) AS average_installments
FROM order_payments;


-- 8. Average installments by payment method
SELECT
    payment_type,
    AVG(payment_installments) AS average_installments
FROM order_payments
GROUP BY payment_type
ORDER BY average_installments DESC;


-- 9. Join orders and payments
SELECT
    o.order_id,
    o.order_status,
    p.payment_type,
    p.payment_value
FROM orders AS o
INNER JOIN order_payments AS p
    ON o.order_id = p.order_id
LIMIT 10;