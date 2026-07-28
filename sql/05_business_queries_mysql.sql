/*
===============================================================================
BLINKIT (QUICK COMMERCE) MASTER ANALYTICS SCRIPT (MySQL 8.0)
===============================================================================
Objective: Provide the data backbone for an Executive Dashboard.
Target KPIs: GMV, MoM Growth, SLA %, RFM Segments, Cohort Retention.
===============================================================================
*/

-- ----------------------------------------------------------------------------
-- PILLAR 1: EXECUTIVE REVENUE OVERVIEW
-- ----------------------------------------------------------------------------

/* 1. Month-over-Month Growth */
use blinkit_analysis ;

WITH MonthlyStats AS (
    SELECT
        DATE_FORMAT(order_datetime,'%Y-%m-01') AS month,
        SUM(total_paid) AS net_revenue,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(total_paid)/COUNT(DISTINCT order_id),2) AS aov
    FROM orders
    WHERE order_status='Delivered'
    GROUP BY DATE_FORMAT(order_datetime,'%Y-%m-01')
)
SELECT
    month,
    net_revenue,
    LAG(net_revenue) OVER(ORDER BY month) AS prev_month_rev,
    ROUND(
        ((net_revenue-LAG(net_revenue) OVER(ORDER BY month))
        /LAG(net_revenue) OVER(ORDER BY month))*100,2
    ) AS revenue_growth_pct,
    aov
FROM MonthlyStats;

-- 2. Revenue Share by City & Membership
SELECT
    c.city,
    c.membership_type,
    SUM(o.total_paid) AS total_revenue,
    ROUND(
        100*SUM(o.total_paid)/SUM(SUM(o.total_paid)) OVER(),2
    ) AS revenue_share_pct
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
GROUP BY c.city,c.membership_type
ORDER BY total_revenue DESC;



-- ----------------------------------------------------------------------------
-- PILLAR 2: OPERATIONAL EFFICIENCY
-- ----------------------------------------------------------------------------

-- 3. SLA Breach Analysis
SELECT
    weather,
    traffic_level,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time,

    SUM(
        CASE
            WHEN actual_delivery_minutes > promised_delivery_minutes
            THEN 1
            ELSE 0
        END
    ) AS breaches,

    ROUND(
        100 *
        SUM(
            CASE
                WHEN actual_delivery_minutes > promised_delivery_minutes
                THEN 1
                ELSE 0
            END
        ) / COUNT(order_id),
    2) AS breach_rate_pct

FROM orders

WHERE order_status='Delivered'

GROUP BY weather,traffic_level;
-- 4. Hourly Demand
SELECT
    HOUR(order_datetime) AS hour_of_day,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_speed
FROM orders
GROUP BY HOUR(order_datetime)
ORDER BY hour_of_day;

-- 5. Store Utilization
SELECT
    s.store_id,
    s.city,
    s.warehouse_capacity,
    COUNT(o.order_id) AS total_orders,
    ROUND(
        CAST(COUNT(o.order_id) AS DECIMAL(10,2))/s.warehouse_capacity,
        2
    ) AS stress_index
FROM orders o
JOIN stores s ON o.store_id=s.store_id
GROUP BY s.store_id,s.city,s.warehouse_capacity
ORDER BY stress_index DESC;

-- ----------------------------------------------------------------------------
-- PILLAR 3: CUSTOMER LOYALTY
-- ----------------------------------------------------------------------------

-- 6. RFM Segmentation
WITH RFM_Base AS (
SELECT
customer_id,
DATEDIFF((SELECT MAX(order_datetime) FROM orders),MAX(order_datetime)) AS recency,
COUNT(order_id) AS frequency,
SUM(total_paid) AS monetary
FROM orders
WHERE order_status='Delivered'
GROUP BY customer_id
)
SELECT
customer_id,
NTILE(5) OVER(ORDER BY recency ASC) AS r_score,
NTILE(5) OVER(ORDER BY frequency DESC) AS f_score,
NTILE(5) OVER(ORDER BY monetary DESC) AS m_score
FROM RFM_Base;

-- 7. Cohort Retention
WITH FirstOrder AS(
SELECT
customer_id,
DATE_FORMAT(MIN(order_datetime),'%Y-%m-01') AS cohort_month
FROM orders
GROUP BY customer_id
),
OrderActivity AS(
SELECT
o.customer_id,
f.cohort_month,
TIMESTAMPDIFF(
MONTH,
f.cohort_month,
DATE_FORMAT(o.order_datetime,'%Y-%m-01')
) AS month_number
FROM orders o
JOIN FirstOrder f
ON o.customer_id=f.customer_id
)
SELECT
cohort_month,
month_number,
COUNT(DISTINCT customer_id) AS active_users
FROM OrderActivity
GROUP BY cohort_month,month_number
ORDER BY cohort_month,month_number;

-- 8. Acquisition Channel LTV
SELECT
c.acquisition_channel,
COUNT(DISTINCT c.customer_id) AS total_users,
SUM(o.total_paid)/COUNT(DISTINCT c.customer_id) AS customer_ltv
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.acquisition_channel
ORDER BY customer_ltv DESC;

-- ----------------------------------------------------------------------------
-- PILLAR 4: PRODUCT ANALYTICS
-- ----------------------------------------------------------------------------

-- 9. Top 3 Products per Category
WITH CategoryRanking AS(
SELECT
p.category,
p.product_name,
SUM(oi.total_price) AS sales_value,
DENSE_RANK() OVER(
PARTITION BY p.category
ORDER BY SUM(oi.total_price) DESC
) AS product_rank
FROM order_items oi
JOIN products p
ON oi.product_id=p.product_id
GROUP BY p.category,p.product_name
)
SELECT *
FROM CategoryRanking
WHERE product_rank<=3;

-- 10. Pareto Analysis
WITH ProductRevenue AS(
SELECT
product_id,
SUM(total_price) AS revenue
FROM order_items
GROUP BY product_id
),
RunningRevenue AS(
SELECT
product_id,
revenue,
SUM(revenue) OVER(ORDER BY revenue DESC) AS running_total,
SUM(revenue) OVER() AS grand_total
FROM ProductRevenue
)
SELECT
product_id,
revenue,
ROUND((running_total/grand_total)*100,2) AS cumulative_percentage
FROM RunningRevenue
WHERE running_total/grand_total<=0.80;

-- ----------------------------------------------------------------------------
-- PILLAR 5: LOGISTICS & FINANCE
-- ----------------------------------------------------------------------------

-- 11. Delivery Partner Performance
SELECT
    delivery_partner_id,
    ROUND(AVG(customer_rating),2) AS avg_rating,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_speed,

    ROUND(
        SUM(
            CASE
                WHEN actual_delivery_minutes <= promised_delivery_minutes
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
    4) AS sla_compliance_rate

FROM orders

WHERE order_status = 'Delivered'

GROUP BY delivery_partner_id

HAVING COUNT(*) > 20

ORDER BY sla_compliance_rate DESC, avg_rating DESC;

-- 12. Coupon Effectiveness
SELECT
CASE
WHEN coupon_id IS NOT NULL THEN 'Coupon Used'
ELSE 'No Coupon'
END AS promo_status,
COUNT(*) AS total_orders,
AVG(order_value) AS avg_basket_value
FROM orders
GROUP BY promo_status;

-- 13. Weekend vs Weekday
SELECT
CASE
WHEN DAYOFWEEK(order_datetime) IN (1,7)
THEN 'Weekend'
ELSE 'Weekday'
END AS day_type,
SUM(total_paid) AS total_revenue,
AVG(total_paid) AS aov
FROM orders
GROUP BY day_type;

-- 14. Cancellation Analysis
SELECT
cancellation_reason,
COUNT(*) AS total_cancellations,
SUM(order_value) AS lost_revenue_gmv
FROM orders
WHERE order_status='Cancelled'
GROUP BY cancellation_reason;
