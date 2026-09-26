-- =========================================================
-- LESSON 19: GEOLOCATION ANALYSIS
-- AI-POWERED CUSTOMER RETENTION & BUSINESS INTELLIGENCE
-- =========================================================


-- =========================================================
-- PART 1: BASIC GEOLOCATION ANALYSIS
-- =========================================================

-- 1. Count total geolocation records
SELECT COUNT(*) AS total_geolocation_records
FROM geolocation;


-- 2. Display sample records
SELECT *
FROM geolocation
LIMIT 10;


-- 3. Display distinct states
SELECT DISTINCT geolocation_state
FROM geolocation
ORDER BY geolocation_state;


-- 4. Count records by state
SELECT
    geolocation_state,
    COUNT(*) AS location_records
FROM geolocation
GROUP BY geolocation_state
ORDER BY location_records DESC;


-- 5. Count records by city
SELECT
    geolocation_city,
    COUNT(*) AS location_records
FROM geolocation
GROUP BY geolocation_city
ORDER BY location_records DESC
LIMIT 20;


-- 6. Count unique ZIP-code prefixes
SELECT
    COUNT(DISTINCT geolocation_zip_code_prefix)
    AS unique_zip_prefixes
FROM geolocation;


-- 7. Count unique cities
SELECT
    COUNT(DISTINCT geolocation_city) AS unique_cities
FROM geolocation;


-- 8. Count unique states
SELECT
    COUNT(DISTINCT geolocation_state) AS unique_states
FROM geolocation;



-- =========================================================
-- PART 2: LATITUDE AND LONGITUDE ANALYSIS
-- =========================================================

-- 9. Minimum and maximum latitude
SELECT
    MIN(geolocation_lat) AS minimum_latitude,
    MAX(geolocation_lat) AS maximum_latitude
FROM geolocation;


-- 10. Minimum and maximum longitude
SELECT
    MIN(geolocation_lng) AS minimum_longitude,
    MAX(geolocation_lng) AS maximum_longitude
FROM geolocation;


-- 11. Average latitude and longitude
SELECT
    ROUND(AVG(geolocation_lat), 6) AS average_latitude,
    ROUND(AVG(geolocation_lng), 6) AS average_longitude
FROM geolocation;


-- 12. Average coordinates by state
SELECT
    geolocation_state,
    ROUND(AVG(geolocation_lat), 6) AS average_latitude,
    ROUND(AVG(geolocation_lng), 6) AS average_longitude
FROM geolocation
GROUP BY geolocation_state
ORDER BY geolocation_state;



-- =========================================================
-- PART 3: CITY-LEVEL GEOLOCATION ANALYSIS
-- =========================================================

-- 13. Top 20 cities by number of location records
SELECT
    geolocation_city,
    geolocation_state,
    COUNT(*) AS location_records
FROM geolocation
GROUP BY geolocation_city, geolocation_state
ORDER BY location_records DESC
LIMIT 20;


-- 14. Cities with more than 1,000 location records
SELECT
    geolocation_city,
    geolocation_state,
    COUNT(*) AS location_records
FROM geolocation
GROUP BY geolocation_city, geolocation_state
HAVING COUNT(*) > 1000
ORDER BY location_records DESC;


-- 15. Number of ZIP prefixes by state
SELECT
    geolocation_state,
    COUNT(DISTINCT geolocation_zip_code_prefix)
        AS unique_zip_prefixes
FROM geolocation
GROUP BY geolocation_state
ORDER BY unique_zip_prefixes DESC;



-- =========================================================
-- PART 4: CUSTOMER LOCATION ANALYSIS
-- =========================================================

-- 16. Customer count by state
SELECT
    c.customer_state,
    COUNT(*) AS customer_count
FROM customers AS c
GROUP BY c.customer_state
ORDER BY customer_count DESC;


-- 17. Customer count by city
SELECT
    c.customer_city,
    c.customer_state,
    COUNT(*) AS customer_count
FROM customers AS c
GROUP BY c.customer_city, c.customer_state
ORDER BY customer_count DESC
LIMIT 20;


-- 18. Customer count by ZIP-code prefix
SELECT
    c.customer_zip_code_prefix,
    COUNT(*) AS customer_count
FROM customers AS c
GROUP BY c.customer_zip_code_prefix
ORDER BY customer_count DESC
LIMIT 20;


-- 19. Customers and their geolocation records
SELECT
    c.customer_id,
    c.customer_zip_code_prefix,
    c.customer_city,
    c.customer_state,
    g.geolocation_lat,
    g.geolocation_lng
FROM customers AS c
INNER JOIN geolocation AS g
    ON c.customer_zip_code_prefix =
       g.geolocation_zip_code_prefix
LIMIT 20;



-- =========================================================
-- PART 5: SELLER LOCATION ANALYSIS
-- =========================================================

-- 20. Seller count by state
SELECT
    s.seller_state,
    COUNT(*) AS seller_count
FROM sellers AS s
GROUP BY s.seller_state
ORDER BY seller_count DESC;


-- 21. Seller count by city
SELECT
    s.seller_city,
    s.seller_state,
    COUNT(*) AS seller_count
FROM sellers AS s
GROUP BY s.seller_city, s.seller_state
ORDER BY seller_count DESC
LIMIT 20;


-- 22. Seller count by ZIP-code prefix
SELECT
    s.seller_zip_code_prefix,
    COUNT(*) AS seller_count
FROM sellers AS s
GROUP BY s.seller_zip_code_prefix
ORDER BY seller_count DESC
LIMIT 20;



-- =========================================================
-- PART 6: CUSTOMER VS SELLER LOCATION ANALYSIS
-- =========================================================

-- 23. Compare customer and seller counts by state
SELECT
    state,
    SUM(customer_count) AS customer_count,
    SUM(seller_count) AS seller_count
FROM
(
    SELECT
        customer_state AS state,
        COUNT(*) AS customer_count,
        0 AS seller_count
    FROM customers
    GROUP BY customer_state

    UNION ALL

    SELECT
        seller_state AS state,
        0 AS customer_count,
        COUNT(*) AS seller_count
    FROM sellers
    GROUP BY seller_state
) AS location_summary
GROUP BY state
ORDER BY customer_count DESC;


-- 24. States with more customers than sellers
SELECT
    state,
    SUM(customer_count) AS customer_count,
    SUM(seller_count) AS seller_count
FROM
(
    SELECT
        customer_state AS state,
        COUNT(*) AS customer_count,
        0 AS seller_count
    FROM customers
    GROUP BY customer_state

    UNION ALL

    SELECT
        seller_state AS state,
        0 AS customer_count,
        COUNT(*) AS seller_count
    FROM sellers
    GROUP BY seller_state
) AS location_summary
GROUP BY state
HAVING SUM(customer_count) > SUM(seller_count)
ORDER BY customer_count DESC;


-- 25. States with sellers but fewer customers
SELECT
    state,
    SUM(customer_count) AS customer_count,
    SUM(seller_count) AS seller_count
FROM
(
    SELECT
        customer_state AS state,
        COUNT(*) AS customer_count,
        0 AS seller_count
    FROM customers
    GROUP BY customer_state

    UNION ALL

    SELECT
        seller_state AS state,
        0 AS customer_count,
        COUNT(*) AS seller_count
    FROM sellers
    GROUP BY seller_state
) AS location_summary
GROUP BY state
HAVING SUM(seller_count) > SUM(customer_count)
ORDER BY seller_count DESC;



-- =========================================================
-- PART 7: GEOLOCATION + CUSTOMER ANALYSIS
-- =========================================================

-- 26. Customers by state with average latitude
SELECT
    c.customer_state,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    ROUND(AVG(g.geolocation_lat), 6) AS average_latitude,
    ROUND(AVG(g.geolocation_lng), 6) AS average_longitude
FROM customers AS c
INNER JOIN geolocation AS g
    ON c.customer_zip_code_prefix =
       g.geolocation_zip_code_prefix
GROUP BY c.customer_state
ORDER BY customer_count DESC;


-- 27. Customer cities with geolocation information
SELECT
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    ROUND(AVG(g.geolocation_lat), 6) AS average_latitude,
    ROUND(AVG(g.geolocation_lng), 6) AS average_longitude
FROM customers AS c
INNER JOIN geolocation AS g
    ON c.customer_zip_code_prefix =
       g.geolocation_zip_code_prefix
GROUP BY c.customer_city, c.customer_state
ORDER BY customer_count DESC
LIMIT 20;



-- =========================================================
-- PART 8: GEOLOCATION + SELLER ANALYSIS
-- =========================================================

-- 28. Sellers with geolocation information
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    g.geolocation_lat,
    g.geolocation_lng
FROM sellers AS s
INNER JOIN geolocation AS g
    ON s.seller_zip_code_prefix =
       g.geolocation_zip_code_prefix
LIMIT 20;


-- 29. Seller states with average coordinates
SELECT
    s.seller_state,
    COUNT(DISTINCT s.seller_id) AS seller_count,
    ROUND(AVG(g.geolocation_lat), 6) AS average_latitude,
    ROUND(AVG(g.geolocation_lng), 6) AS average_longitude
FROM sellers AS s
INNER JOIN geolocation AS g
    ON s.seller_zip_code_prefix =
       g.geolocation_zip_code_prefix
GROUP BY s.seller_state
ORDER BY seller_count DESC;



-- =========================================================
-- PART 9: BUSINESS INSIGHTS
-- =========================================================

-- 30. Top customer states
SELECT
    customer_state,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_state
ORDER BY customer_count DESC
LIMIT 10;


-- 31. Top seller states
SELECT
    seller_state,
    COUNT(*) AS seller_count
FROM sellers
GROUP BY seller_state
ORDER BY seller_count DESC
LIMIT 10;


-- 32. Customer concentration by state
SELECT
    customer_state,
    COUNT(*) AS customer_count,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM customers),
        2
    ) AS customer_percentage
FROM customers
GROUP BY customer_state
ORDER BY customer_percentage DESC;


-- 33. Seller concentration by state
SELECT
    seller_state,
    COUNT(*) AS seller_count,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM sellers),
        2
    ) AS seller_percentage
FROM sellers
GROUP BY seller_state
ORDER BY seller_percentage DESC;



-- =========================================================
-- PART 10: FINAL GEOLOCATION SUMMARY
-- =========================================================

-- 34. Overall geolocation summary
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT geolocation_zip_code_prefix)
        AS unique_zip_prefixes,
    COUNT(DISTINCT geolocation_city)
        AS unique_cities,
    COUNT(DISTINCT geolocation_state)
        AS unique_states,
    ROUND(AVG(geolocation_lat), 6)
        AS average_latitude,
    ROUND(AVG(geolocation_lng), 6)
        AS average_longitude
FROM geolocation;


-- 35. State-level geographical summary
SELECT
    geolocation_state,
    COUNT(*) AS location_records,
    COUNT(DISTINCT geolocation_zip_code_prefix)
        AS unique_zip_prefixes,
    COUNT(DISTINCT geolocation_city)
        AS unique_cities,
    ROUND(AVG(geolocation_lat), 6)
        AS average_latitude,
    ROUND(AVG(geolocation_lng), 6)
        AS average_longitude
FROM geolocation
GROUP BY geolocation_state
ORDER BY location_records DESC;