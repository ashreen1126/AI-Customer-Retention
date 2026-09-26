-- =========================================================
-- LESSON 18: ORDER REVIEWS & CUSTOMER SATISFACTION ANALYSIS
-- =========================================================


-- =========================================================
-- PART 1: CREATE ORDER REVIEWS TABLE
-- =========================================================

CREATE TABLE order_reviews (
    review_pk BIGSERIAL PRIMARY KEY,
    review_id TEXT,
    order_id TEXT,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =========================================================
-- PART 2: BASIC REVIEW ANALYSIS
-- =========================================================

-- 1. Count total reviews
SELECT COUNT(*) AS total_reviews
FROM order_reviews;


-- 2. View sample reviews
SELECT *
FROM order_reviews
LIMIT 10;


-- 3. Check review score values
SELECT DISTINCT review_score
FROM order_reviews
ORDER BY review_score;


-- 4. Count reviews for each score
SELECT
    review_score,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;


-- 5. Calculate average review score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews;


-- =========================================================
-- PART 3: POSITIVE, NEUTRAL & NEGATIVE REVIEWS
-- =========================================================

-- 6. Count positive reviews (4–5 stars)
SELECT COUNT(*) AS positive_reviews
FROM order_reviews
WHERE review_score >= 4;


-- 7. Count neutral reviews (3 stars)
SELECT COUNT(*) AS neutral_reviews
FROM order_reviews
WHERE review_score = 3;


-- 8. Count negative reviews (1–2 stars)
SELECT COUNT(*) AS negative_reviews
FROM order_reviews
WHERE review_score <= 2;


-- 9. Positive review percentage
SELECT
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM order_reviews),
        2
    ) AS positive_percentage
FROM order_reviews
WHERE review_score >= 4;


-- 10. Neutral review percentage
SELECT
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM order_reviews),
        2
    ) AS neutral_percentage
FROM order_reviews
WHERE review_score = 3;


-- 11. Negative review percentage
SELECT
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM order_reviews),
        2
    ) AS negative_percentage
FROM order_reviews
WHERE review_score <= 2;


-- =========================================================
-- PART 4: REVIEW & ORDER ANALYSIS
-- =========================================================

-- 12. Reviews by order
SELECT
    order_id,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY order_id
ORDER BY review_count DESC
LIMIT 10;


-- 13. Connect reviews with orders
SELECT
    r.review_id,
    r.review_score,
    o.order_id,
    o.customer_id,
    o.order_status
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
LIMIT 10;


-- 14. Average review score by order status
SELECT
    o.order_status,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.review_score), 2) AS average_review_score
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
GROUP BY o.order_status
ORDER BY average_review_score DESC;


-- 15. Review scores by order status
SELECT
    o.order_status,
    r.review_score,
    COUNT(*) AS review_count
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
GROUP BY
    o.order_status,
    r.review_score
ORDER BY
    o.order_status,
    r.review_score;


-- =========================================================
-- PART 5: REVIEW & CUSTOMER ANALYSIS
-- =========================================================

-- 16. Find customers with their review scores
SELECT
    o.customer_id,
    r.review_score,
    r.review_creation_date
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
LIMIT 20;


-- 17. Average review score by customer
SELECT
    o.customer_id,
    ROUND(AVG(r.review_score), 2) AS average_review_score,
    COUNT(r.review_id) AS number_of_reviews
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY average_review_score DESC
LIMIT 20;


-- 18. Customers with low review scores
SELECT
    o.customer_id,
    r.review_score,
    r.review_comment_message
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
WHERE r.review_score <= 2
LIMIT 20;


-- 19. Customers with multiple reviews
SELECT
    o.customer_id,
    COUNT(r.review_id) AS number_of_reviews
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
GROUP BY o.customer_id
HAVING COUNT(r.review_id) > 1
ORDER BY number_of_reviews DESC
LIMIT 20;


-- =========================================================
-- PART 6: REVIEW COMMENTS
-- =========================================================

-- 20. Count reviews with comments
SELECT COUNT(*) AS reviews_with_comments
FROM order_reviews
WHERE review_comment_message IS NOT NULL
  AND TRIM(review_comment_message) <> '';


-- 21. Count reviews without comments
SELECT COUNT(*) AS reviews_without_comments
FROM order_reviews
WHERE review_comment_message IS NULL
   OR TRIM(review_comment_message) = '';


-- 22. View negative reviews with customer information
SELECT
    o.customer_id,
    r.review_score,
    r.review_comment_title,
    r.review_comment_message
FROM order_reviews AS r
INNER JOIN orders AS o
    ON r.order_id = o.order_id
WHERE r.review_score <= 2
LIMIT 20;


-- =========================================================
-- PART 7: TIME-BASED REVIEW ANALYSIS
-- =========================================================

-- 23. Review count by year
SELECT
    EXTRACT(YEAR FROM review_creation_date) AS review_year,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY review_year
ORDER BY review_year;


-- 24. Average review score by year
SELECT
    EXTRACT(YEAR FROM review_creation_date) AS review_year,
    ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews
GROUP BY review_year
ORDER BY review_year;


-- 25. Review count by month
SELECT
    EXTRACT(YEAR FROM review_creation_date) AS review_year,
    EXTRACT(MONTH FROM review_creation_date) AS review_month,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY
    review_year,
    review_month
ORDER BY
    review_year,
    review_month;


-- =========================================================
-- PART 8: REVIEW SCORE DISTRIBUTION
-- =========================================================

-- 26. Review count and percentage for each score
SELECT
    review_score,
    COUNT(*) AS review_count,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM order_reviews),
        2
    ) AS percentage
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;


-- 27. Overall customer satisfaction summary
SELECT
    COUNT(*) AS total_reviews,
    ROUND(AVG(review_score), 2) AS average_score,

    COUNT(*) FILTER (
        WHERE review_score >= 4
    ) AS positive_reviews,

    COUNT(*) FILTER (
        WHERE review_score = 3
    ) AS neutral_reviews,

    COUNT(*) FILTER (
        WHERE review_score <= 2
    ) AS negative_reviews

FROM order_reviews;


-- =========================================================
-- PART 9: CUSTOMER SATISFACTION CATEGORY
-- =========================================================

-- 28. Classify every review
SELECT
    review_id,
    review_score,
    CASE
        WHEN review_score >= 4 THEN 'Positive'
        WHEN review_score = 3 THEN 'Neutral'
        WHEN review_score <= 2 THEN 'Negative'
    END AS satisfaction_category
FROM order_reviews
LIMIT 20;


-- 29. Count reviews by satisfaction category
SELECT
    CASE
        WHEN review_score >= 4 THEN 'Positive'
        WHEN review_score = 3 THEN 'Neutral'
        WHEN review_score <= 2 THEN 'Negative'
    END AS satisfaction_category,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY satisfaction_category
ORDER BY review_count DESC;


-- =========================================================
-- PART 10: FINAL REVIEW ANALYSIS
-- =========================================================

-- 30. Complete customer satisfaction summary
SELECT
    COUNT(*) AS total_reviews,

    ROUND(AVG(review_score), 2)
        AS average_review_score,

    COUNT(*) FILTER (
        WHERE review_score >= 4
    ) AS positive_reviews,

    COUNT(*) FILTER (
        WHERE review_score = 3
    ) AS neutral_reviews,

    COUNT(*) FILTER (
        WHERE review_score <= 2
    ) AS negative_reviews,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE review_score >= 4
        ) / COUNT(*),
        2
    ) AS positive_percentage,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE review_score <= 2
        ) / COUNT(*),
        2
    ) AS negative_percentage

FROM order_reviews;