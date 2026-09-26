-- ============================================================
-- LESSON 15: ORDER ITEMS & PRODUCT SALES ANALYSIS
-- Project: AI-Powered Customer Retention & Business Intelligence Platform
-- Database: customer_retention
-- ============================================================


-- ============================================================
-- 1. CHECK TOTAL ORDER-ITEM RECORDS
-- ============================================================

SELECT
    COUNT(*) AS total_order_items
FROM order_items;


-- ============================================================
-- 2. VIEW SAMPLE ORDER-ITEM DATA
-- ============================================================

SELECT *
FROM order_items
LIMIT 10;


-- ============================================================
-- 3. CALCULATE TOTAL PRODUCT SALES
-- ============================================================

SELECT
    SUM(price) AS total_sales
FROM order_items;


-- ============================================================
-- 4. CALCULATE AVERAGE PRODUCT PRICE
-- ============================================================

SELECT
    AVG(price) AS average_product_price
FROM order_items;


-- ============================================================
-- 5. CALCULATE TOTAL FREIGHT VALUE
-- ============================================================

SELECT
    SUM(freight_value) AS total_freight
FROM order_items;


-- ============================================================
-- 6. CALCULATE AVERAGE FREIGHT VALUE
-- ============================================================

SELECT
    AVG(freight_value) AS average_freight
FROM order_items;


-- ============================================================
-- 7. FIND THE 10 MOST EXPENSIVE ORDER ITEMS
-- ============================================================

SELECT
    order_id,
    product_id,
    price,
    freight_value
FROM order_items
ORDER BY price DESC
LIMIT 10;


-- ============================================================
-- 8. CALCULATE TOTAL ITEM COST
-- Product Price + Freight
-- ============================================================

SELECT
    order_id,
    product_id,
    price,
    freight_value,
    (price + freight_value) AS total_item_cost
FROM order_items
ORDER BY total_item_cost DESC
LIMIT 10;


-- ============================================================
-- 9. JOIN ORDERS WITH ORDER ITEMS
-- ============================================================

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    oi.product_id,
    oi.price,
    oi.freight_value
FROM orders AS o
INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id
LIMIT 10;


-- ============================================================
-- 10. TOTAL SALES AND FREIGHT FOR EACH ORDER
-- ============================================================

SELECT
    order_id,
    SUM(price) AS order_product_value,
    SUM(freight_value) AS order_freight
FROM order_items
GROUP BY order_id
ORDER BY order_product_value DESC
LIMIT 10;


-- ============================================================
-- 11. TOTAL VALUE INCLUDING FREIGHT FOR EACH ORDER
-- ============================================================

SELECT
    order_id,
    SUM(price) AS product_value,
    SUM(freight_value) AS freight_value,
    SUM(price + freight_value) AS total_order_value
FROM order_items
GROUP BY order_id
ORDER BY total_order_value DESC
LIMIT 10;


-- ============================================================
-- 12. COUNT ITEMS IN EACH ORDER
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS number_of_items
FROM order_items
GROUP BY order_id
ORDER BY number_of_items DESC
LIMIT 10;


-- ============================================================
-- 13. AVERAGE PRODUCT PRICE BY SELLER
-- ============================================================

SELECT
    seller_id,
    AVG(price) AS average_product_price
FROM order_items
GROUP BY seller_id
ORDER BY average_product_price DESC
LIMIT 10;


-- ============================================================
-- 14. TOTAL SALES BY SELLER
-- ============================================================

SELECT
    seller_id,
    SUM(price) AS total_sales
FROM order_items
GROUP BY seller_id
ORDER BY total_sales DESC
LIMIT 10;


-- ============================================================
-- 15. TOTAL FREIGHT BY SELLER
-- ============================================================

SELECT
    seller_id,
    SUM(freight_value) AS total_freight
FROM order_items
GROUP BY seller_id
ORDER BY total_freight DESC
LIMIT 10;


-- ============================================================
-- END OF LESSON 15
-- ============================================================