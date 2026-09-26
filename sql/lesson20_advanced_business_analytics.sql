-- =========================================================
-- LESSON 20: ADVANCED SQL BUSINESS ANALYTICS
-- AI-POWERED CUSTOMER RETENTION & BUSINESS INTELLIGENCE
-- =========================================================


-- =========================================================
-- PART 1: OVERALL BUSINESS ANALYSIS
-- =========================================================

-- 1. Total product revenue
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;


-- 2. Total number of orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- 3. Total number of customers
SELECT
    COUNT(DISTINCT customer_id) AS total_customers
FROM customers;


-- 4. Average order value
SELECT
    ROUND(
        SUM(price) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM order_items;


-- 5. Total freight cost
SELECT
    ROUND(SUM(freight_value), 2) AS total_freight
FROM order_items;



-- =========================================================
-- PART 2: MONTHLY REVENUE ANALYSIS
-- =========================================================

-- 6. Monthly revenue
SELECT
    DATE_TRUNC(
        'month',
        o.order_purchase_timestamp
    ) AS month,

    ROUND(SUM(oi.price), 2) AS monthly_revenue

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY month

ORDER BY month;


-- 7. Monthly number of orders
SELECT
    DATE_TRUNC(
        'month',
        order_purchase_timestamp
    ) AS month,

    COUNT(DISTINCT order_id) AS total_orders

FROM orders

GROUP BY month

ORDER BY month;


-- 8. Monthly average order value
SELECT
    DATE_TRUNC(
        'month',
        o.order_purchase_timestamp
    ) AS month,

    ROUND(
        SUM(oi.price) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY month

ORDER BY month;



-- =========================================================
-- PART 3: TOP CUSTOMERS
-- =========================================================

-- 9. Top 20 customers by total spending
SELECT
    o.customer_id,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_spending

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY o.customer_id

ORDER BY total_spending DESC

LIMIT 20;


-- 10. Top 20 customers by number of orders
SELECT
    customer_id,

    COUNT(DISTINCT order_id)
        AS number_of_orders

FROM orders

GROUP BY customer_id

ORDER BY number_of_orders DESC

LIMIT 20;


-- 11. Customer spending and order frequency
SELECT
    o.customer_id,

    COUNT(DISTINCT o.order_id)
        AS number_of_orders,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_spending,

    ROUND(
        SUM(oi.price) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY o.customer_id

ORDER BY total_spending DESC

LIMIT 20;



-- =========================================================
-- PART 4: REPEAT CUSTOMER ANALYSIS
-- =========================================================

-- 12. Number of repeat customers
SELECT
    COUNT(*) AS repeat_customers

FROM
(
    SELECT
        customer_id

    FROM orders

    GROUP BY customer_id

    HAVING COUNT(DISTINCT order_id) > 1
) AS repeat_customer_list;


-- 13. Number of one-time customers
SELECT
    COUNT(*) AS one_time_customers

FROM
(
    SELECT
        customer_id

    FROM orders

    GROUP BY customer_id

    HAVING COUNT(DISTINCT order_id) = 1
) AS one_time_customer_list;


-- 14. Repeat customers with their order count
SELECT
    customer_id,

    COUNT(DISTINCT order_id)
        AS number_of_orders

FROM orders

GROUP BY customer_id

HAVING COUNT(DISTINCT order_id) > 1

ORDER BY number_of_orders DESC;



-- =========================================================
-- PART 5: PRODUCT CATEGORY ANALYSIS
-- =========================================================

-- 15. Top categories by revenue
SELECT
    p.product_category_name,

    COUNT(*) AS items_sold,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_revenue

FROM order_items AS oi

INNER JOIN products AS p
    ON oi.product_id = p.product_id

GROUP BY p.product_category_name

ORDER BY total_revenue DESC

LIMIT 20;


-- 16. Top categories by number of items sold
SELECT
    p.product_category_name,

    COUNT(*) AS items_sold

FROM order_items AS oi

INNER JOIN products AS p
    ON oi.product_id = p.product_id

GROUP BY p.product_category_name

ORDER BY items_sold DESC

LIMIT 20;


-- 17. Average product price by category
SELECT
    p.product_category_name,

    ROUND(
        AVG(oi.price),
        2
    ) AS average_price

FROM order_items AS oi

INNER JOIN products AS p
    ON oi.product_id = p.product_id

GROUP BY p.product_category_name

ORDER BY average_price DESC

LIMIT 20;


-- 18. Top sellers by revenue
SELECT
    oi.seller_id,

    COUNT(DISTINCT oi.order_id)
        AS number_of_orders,

    COUNT(*) AS items_sold,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_sales

FROM order_items AS oi

GROUP BY oi.seller_id

ORDER BY total_sales DESC

LIMIT 20;


-- 19. Top sellers by number of items sold
SELECT
    seller_id,

    COUNT(*) AS items_sold

FROM order_items

GROUP BY seller_id

ORDER BY items_sold DESC

LIMIT 20;


-- 20. Seller revenue with location
SELECT
    s.seller_id,

    s.seller_city,

    s.seller_state,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_sales

FROM sellers AS s

INNER JOIN order_items AS oi
    ON s.seller_id = oi.seller_id

GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state

ORDER BY total_sales DESC

LIMIT 20;



-- =========================================================
-- PART 7: CUSTOMER SATISFACTION + SPENDING
-- =========================================================

-- 21. Customer spending and review score
SELECT
    o.customer_id,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_spending,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN order_reviews AS r
    ON o.order_id = r.order_id

GROUP BY o.customer_id

ORDER BY total_spending DESC

LIMIT 20;


-- 22. Average spending by review score
SELECT
    r.review_score,

    COUNT(DISTINCT o.customer_id)
        AS customers,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_revenue,

    ROUND(
        AVG(oi.price),
        2
    ) AS average_item_price

FROM order_reviews AS r

INNER JOIN orders AS o
    ON r.order_id = o.order_id

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY r.review_score

ORDER BY r.review_score;



-- =========================================================
-- PART 8: HIGH-VALUE CUSTOMER ANALYSIS
-- =========================================================

-- 23. Classify customers by spending
SELECT
    customer_id,

    number_of_orders,

    total_spending,

    CASE
        WHEN total_spending >= 1000
            THEN 'High Value'

        WHEN total_spending >= 500
            THEN 'Medium Value'

        ELSE 'Low Value'
    END AS customer_value

FROM
(
    SELECT
        o.customer_id,

        COUNT(DISTINCT o.order_id)
            AS number_of_orders,

        ROUND(
            SUM(oi.price),
            2
        ) AS total_spending

    FROM orders AS o

    INNER JOIN order_items AS oi
        ON o.order_id = oi.order_id

    GROUP BY o.customer_id
) AS customer_summary

ORDER BY total_spending DESC;


-- 24. Count customers in each value segment
SELECT
    customer_value,

    COUNT(*) AS customer_count

FROM
(
    SELECT
        customer_id,

        CASE
            WHEN total_spending >= 1000
                THEN 'High Value'

            WHEN total_spending >= 500
                THEN 'Medium Value'

            ELSE 'Low Value'
        END AS customer_value

    FROM
    (
        SELECT
            o.customer_id,

            SUM(oi.price)
                AS total_spending

        FROM orders AS o

        INNER JOIN order_items AS oi
            ON o.order_id = oi.order_id

        GROUP BY o.customer_id
    ) AS spending_data
) AS customer_segments

GROUP BY customer_value

ORDER BY customer_count DESC;



-- =========================================================
-- PART 9: RFM FOUNDATION
-- =========================================================

-- R = Recency
-- F = Frequency
-- M = Monetary Value

-- 25. Basic RFM customer data
SELECT
    o.customer_id,

    MAX(
        o.order_purchase_timestamp
    ) AS last_purchase_date,

    COUNT(
        DISTINCT o.order_id
    ) AS frequency,

    ROUND(
        SUM(oi.price),
        2
    ) AS monetary_value

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY o.customer_id

ORDER BY monetary_value DESC;


-- 26. RFM data with first purchase date
SELECT
    o.customer_id,

    MIN(
        o.order_purchase_timestamp
    ) AS first_purchase_date,

    MAX(
        o.order_purchase_timestamp
    ) AS last_purchase_date,

    COUNT(
        DISTINCT o.order_id
    ) AS frequency,

    ROUND(
        SUM(oi.price),
        2
    ) AS monetary_value

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY o.customer_id;



-- =========================================================
-- PART 10: CUSTOMER RECENCY
-- =========================================================

-- 27. Days since last purchase
SELECT
    customer_id,

    MAX(order_purchase_timestamp)
        AS last_purchase_date,

    CURRENT_DATE -
        MAX(order_purchase_timestamp)::DATE
        AS days_since_last_purchase

FROM orders

GROUP BY customer_id

ORDER BY days_since_last_purchase DESC;



-- =========================================================
-- PART 11: CHURN-RELATED ANALYSIS
-- =========================================================

-- 28. Customers who have not purchased recently
-- This is a simple exploratory rule.
-- Later, the ML model will use a better approach.

SELECT
    customer_id,

    MAX(order_purchase_timestamp)
        AS last_purchase_date,

    CURRENT_DATE -
        MAX(order_purchase_timestamp)::DATE
        AS days_since_last_purchase

FROM orders

GROUP BY customer_id

HAVING
    CURRENT_DATE -
    MAX(order_purchase_timestamp)::DATE > 365

ORDER BY days_since_last_purchase DESC;


-- 29. Customers grouped by recency
SELECT
    customer_id,

    MAX(order_purchase_timestamp)
        AS last_purchase_date,

    CURRENT_DATE -
        MAX(order_purchase_timestamp)::DATE
        AS days_since_last_purchase,

    CASE
        WHEN CURRENT_DATE -
             MAX(order_purchase_timestamp)::DATE <= 90
            THEN 'Recent'

        WHEN CURRENT_DATE -
             MAX(order_purchase_timestamp)::DATE <= 180
            THEN 'Moderately Recent'

        WHEN CURRENT_DATE -
             MAX(order_purchase_timestamp)::DATE <= 365
            THEN 'At Risk'

        ELSE 'Inactive'
    END AS customer_recency_status

FROM orders

GROUP BY customer_id

ORDER BY days_since_last_purchase DESC;



-- =========================================================
-- PART 12: COMPLETE CUSTOMER ANALYTICS TABLE
-- =========================================================

-- 30. Customer-level business summary
SELECT
    o.customer_id,

    MIN(
        o.order_purchase_timestamp
    ) AS first_purchase_date,

    MAX(
        o.order_purchase_timestamp
    ) AS last_purchase_date,

    COUNT(
        DISTINCT o.order_id
    ) AS total_orders,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_spending,

    ROUND(
        SUM(oi.price) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value,

    ROUND(
        AVG(r.review_score),
        2
    ) AS average_review_score

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

LEFT JOIN order_reviews AS r
    ON o.order_id = r.order_id

GROUP BY o.customer_id

ORDER BY total_spending DESC;



-- =========================================================
-- PART 13: WINDOW FUNCTION
-- =========================================================

-- 31. Rank customers by total spending
SELECT
    customer_id,

    total_spending,

    RANK() OVER (
        ORDER BY total_spending DESC
    ) AS spending_rank

FROM
(
    SELECT
        o.customer_id,

        ROUND(
            SUM(oi.price),
            2
        ) AS total_spending

    FROM orders AS o

    INNER JOIN order_items AS oi
        ON o.order_id = oi.order_id

    GROUP BY o.customer_id
) AS customer_spending

ORDER BY spending_rank

LIMIT 20;



-- =========================================================
-- PART 14: CUSTOMER RANK WITH ORDER FREQUENCY
-- =========================================================

-- 32. Rank customers by spending and frequency
SELECT
    customer_id,

    total_orders,

    total_spending,

    RANK() OVER (
        ORDER BY total_spending DESC
    ) AS spending_rank,

    RANK() OVER (
        ORDER BY total_orders DESC
    ) AS frequency_rank

FROM
(
    SELECT
        o.customer_id,

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders,

        ROUND(
            SUM(oi.price),
            2
        ) AS total_spending

    FROM orders AS o

    INNER JOIN order_items AS oi
        ON o.order_id = oi.order_id

    GROUP BY o.customer_id
) AS customer_data

ORDER BY spending_rank

LIMIT 20;



-- =========================================================
-- PART 15: FINAL BUSINESS SUMMARY
-- =========================================================

-- 33. Overall business summary
SELECT

    COUNT(DISTINCT o.order_id)
        AS total_orders,

    COUNT(DISTINCT o.customer_id)
        AS total_customers,

    COUNT(DISTINCT oi.product_id)
        AS unique_products,

    COUNT(DISTINCT oi.seller_id)
        AS unique_sellers,

    ROUND(
        SUM(oi.price),
        2
    ) AS total_revenue,

    ROUND(
        SUM(oi.price) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value,

    ROUND(
        SUM(oi.freight_value),
        2
    ) AS total_freight

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id;



-- =========================================================
-- END OF LESSON 20
-- =========================================================