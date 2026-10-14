SELECT
    variant,
    COUNT(*) AS total_assignment_logs,
    COUNT(DISTINCT user_id) AS total_unique_users
FROM assignments
GROUP BY variant;




WITH user_variants AS (
    SELECT
        user_id,
       COUNT(DISTINCT variant) AS variant_count
    FROM assignments
    GROUP BY user_id)

SELECT
    COUNT(CASE WHEN variant_count > 1 THEN 1 END) AS dual_assigned_users_removed,
    COUNT(DISTINCT user_id) AS total_assigned_users,
    ROUND(
        100.0 * COUNT(CASE WHEN variant_count > 1 THEN 1 END) / COUNT(DISTINCT user_id), 2
    ) AS contamination_rate_pct

FROM user_variants;


WITH first_assignment AS (
    SELECT
        user_id,
        MIN(assigned_at) AS first_assigned_at
    FROM assignments
    GROUP BY user_id
)
SELECT
    COUNT(o.order_id) AS pre_assignment_orders_removed,
    COALESCE(SUM(o.order_value), 0) AS pre_assignment_revenue_removed
FROM orders o
JOIN first_assignment a ON o.user_id = a.user_id
WHERE o.ordered_at < a.first_assigned_at;

WITH clean_assignments AS (
    -- 1. Remove dual-assigned users and keep single clean record per user
    SELECT
        user_id,
        MIN(variant) AS variant,
        MIN(assigned_at) AS assigned_at,
        MIN(device) AS device,
        MIN(visitor_type) AS visitor_type
    FROM assignments
    GROUP BY user_id
    HAVING COUNT(DISTINCT variant) = 1
),

valid_orders AS (
    -- 2. Keep ONLY orders placed AT or AFTER the assignment timestamp
    SELECT
        o.order_id,
        o.user_id,
        o.order_value
    FROM orders o
    JOIN clean_assignments a ON o.user_id = a.user_id
    WHERE o.ordered_at >= a.assigned_at
)

-- 3. Aggregate metrics to the User Level
SELECT
    a.user_id,
    a.variant,
    a.device,
    a.visitor_type,

    -- Primary Metric Component: Binary Conversion (1 = converted, 0 = didn't convert)
    CASE WHEN COUNT(v.order_id) > 0 THEN 1 ELSE 0 END AS converted,

    -- Secondary Metric Component: Total Revenue per User (ARPU)
    COALESCE(SUM(v.order_value), 0) AS user_revenue,

    -- Diagnostic Component: Total post-assignment order count
    COUNT(v.order_id) AS order_count

FROM clean_assignments a
LEFT JOIN valid_orders v ON a.user_id = v.user_id
GROUP BY
    a.user_id,
    a.variant,
    a.device,
    a.visitor_type;