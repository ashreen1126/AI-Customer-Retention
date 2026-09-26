-- ============================================
-- LESSON 17: SELLER & SELLER PERFORMANCE ANALYSIS
-- ============================================


-- 1. Count total sellers
SELECT COUNT(*) AS total_sellers
FROM sellers;


-- 2. View sample sellers
SELECT *
FROM sellers
LIMIT 10;


-- 3. Number of sellers by state
SELECT
    seller_state,
    COUNT(*) AS seller_count
FROM sellers
GROUP BY seller_state
ORDER BY seller_count DESC;


-- 4. Top 10 seller cities
SELECT
    seller_city,
    COUNT(*) AS seller_count
FROM sellers
GROUP BY seller_city
ORDER BY seller_count DESC
LIMIT 10;


-- 5. Top 10 sellers by total sales
SELECT
    seller_id,
    SUM(price) AS total_sales
FROM order_items
GROUP BY seller_id
ORDER BY total_sales DESC
LIMIT 10;


-- 6. Top 10 sellers by items sold
SELECT
    seller_id,
    COUNT(*) AS items_sold
FROM order_items
GROUP BY seller_id
ORDER BY items_sold DESC
LIMIT 10;


-- 7. Top 10 sellers by average product price
SELECT
    seller_id,
    AVG(price) AS average_price
FROM order_items
GROUP BY seller_id
ORDER BY average_price DESC
LIMIT 10;


-- 8. Top 10 sellers by total freight
SELECT
    seller_id,
    SUM(freight_value) AS total_freight
FROM order_items
GROUP BY seller_id
ORDER BY total_freight DESC
LIMIT 10;


-- 9. Seller performance with location
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(*) AS items_sold,
    SUM(oi.price) AS total_sales,
    AVG(oi.price) AS average_price,
    SUM(oi.freight_value) AS total_freight
FROM sellers AS s
INNER JOIN order_items AS oi
    ON s.seller_id = oi.seller_id
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY total_sales DESC
LIMIT 10;


-- 10. Sellers with more than 100 items sold
SELECT
    seller_id,
    COUNT(*) AS items_sold
FROM order_items
GROUP BY seller_id
HAVING COUNT(*) > 100
ORDER BY items_sold DESC;


-- 11. Total sales by seller state
SELECT
    s.seller_state,
    SUM(oi.price) AS total_sales
FROM sellers AS s
INNER JOIN order_items AS oi
    ON s.seller_id = oi.seller_id
GROUP BY s.seller_state
ORDER BY total_sales DESC;


-- 12. Average sales per seller
SELECT
    AVG(total_sales) AS average_seller_sales
FROM (
    SELECT
        seller_id,
        SUM(price) AS total_sales
    FROM order_items
    GROUP BY seller_id
) AS seller_sales;


-- 13. Complete seller performance
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(*) AS items_sold,
    SUM(oi.price) AS total_sales,
    AVG(oi.price) AS average_price,
    SUM(oi.freight_value) AS total_freight
FROM sellers AS s
INNER JOIN order_items AS oi
    ON s.seller_id = oi.seller_id
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY total_sales DESC
LIMIT 10;