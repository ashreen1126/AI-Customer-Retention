-- =========================================================
-- LESSON 16: PRODUCTS & PRODUCT CATEGORY ANALYSIS
-- Project: AI-Powered Customer Retention & Business Intelligence Platform
-- =========================================================


-- 1. Count total products
SELECT COUNT(*) AS total_products
FROM products;


-- 2. View sample products
SELECT *
FROM products
LIMIT 10;


-- 3. Check missing product categories
SELECT COUNT(*) AS missing_categories
FROM products
WHERE product_category_name IS NULL;


-- 4. Count products by category
SELECT
    product_category_name,
    COUNT(*) AS product_count
FROM products
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name
ORDER BY product_count DESC;


-- 5. Find the top 10 product categories
SELECT
    product_category_name,
    COUNT(*) AS product_count
FROM products
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name
ORDER BY product_count DESC
LIMIT 10;


-- 6. Find the least represented product categories
SELECT
    product_category_name,
    COUNT(*) AS product_count
FROM products
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name
ORDER BY product_count ASC
LIMIT 10;


-- 7. Find the most expensive products sold
SELECT
    p.product_id,
    p.product_category_name,
    oi.price
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
ORDER BY oi.price DESC
LIMIT 10;


-- 8. Find the cheapest products sold
SELECT
    p.product_id,
    p.product_category_name,
    oi.price
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
ORDER BY oi.price ASC
LIMIT 10;


-- 9. Calculate average product price
SELECT
    AVG(price) AS average_product_price
FROM order_items;


-- 10. Calculate average price by category
SELECT
    p.product_category_name,
    AVG(oi.price) AS average_price
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY average_price DESC;


-- 11. Find top 10 categories by average price
SELECT
    p.product_category_name,
    AVG(oi.price) AS average_price
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY average_price DESC
LIMIT 10;


-- 12. Find total sales by product category
SELECT
    p.product_category_name,
    SUM(oi.price) AS total_sales
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_sales DESC;


-- 13. Find top 10 categories by total sales
SELECT
    p.product_category_name,
    SUM(oi.price) AS total_sales
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_sales DESC
LIMIT 10;


-- 14. Count items sold by category
SELECT
    p.product_category_name,
    COUNT(*) AS items_sold
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY items_sold DESC;


-- 15. Find categories with more than 1000 items sold
SELECT
    p.product_category_name,
    COUNT(*) AS items_sold
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
HAVING COUNT(*) > 1000
ORDER BY items_sold DESC;


-- 16. Calculate average freight by product category
SELECT
    p.product_category_name,
    AVG(oi.freight_value) AS average_freight
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY average_freight DESC;


-- 17. Calculate total freight by product category
SELECT
    p.product_category_name,
    SUM(oi.freight_value) AS total_freight
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_freight DESC;


-- 18. Find categories with the highest number of different products
SELECT
    product_category_name,
    COUNT(DISTINCT product_id) AS unique_products
FROM products
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name
ORDER BY unique_products DESC
LIMIT 10;


-- 19. Find products that have been sold the most
SELECT
    oi.product_id,
    p.product_category_name,
    COUNT(*) AS times_sold
FROM order_items AS oi
INNER JOIN products AS p
    ON oi.product_id = p.product_id
GROUP BY
    oi.product_id,
    p.product_category_name
ORDER BY times_sold DESC
LIMIT 10;


-- 20. Find total revenue and number of products sold by category
SELECT
    p.product_category_name,
    COUNT(*) AS items_sold,
    SUM(oi.price) AS total_revenue,
    AVG(oi.price) AS average_price
FROM products AS p
INNER JOIN order_items AS oi
    ON p.product_id = oi.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_revenue DESC;