-- ========================================================
-- RetailPulse AI — Production Analytical SQL Views
-- Cross-compatible with PostgreSQL and SQLite
-- ========================================================

-- 1. Master Denormalized Line Items Analytical View
CREATE VIEW IF NOT EXISTS v_analytics_order_items AS
SELECT
    oi.order_item_id,
    oi.order_id,
    o.order_date,
    strftime('%Y-%m', o.order_date) AS order_year_month,
    strftime('%Y', o.order_date) AS order_year,
    o.region,
    o.payment_method,
    o.ship_mode,
    o.order_status,
    c.customer_id,
    c.customer_name,
    c.city,
    c.segment AS customer_segment,
    c.signup_date,
    p.product_id,
    p.product_name,
    cat.category_id,
    cat.category_name,
    oi.quantity,
    oi.unit_price,
    oi.discount,
    oi.line_total AS revenue,
    (oi.quantity * p.cost) AS cogs,
    oi.line_profit AS profit,
    CASE 
        WHEN oi.line_total > 0 THEN ROUND((oi.line_profit / oi.line_total) * 100, 2)
        ELSE 0.00 
    END AS profit_margin_pct
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
JOIN customers c ON o.customer_id = c.customer_id;

-- 2. Monthly Trends and Month-over-Month Growth (with Window Functions)
CREATE VIEW IF NOT EXISTS v_monthly_sales_summary AS
WITH monthly_agg AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS year_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS active_customers,
        SUM(oi.quantity) AS total_units_sold,
        ROUND(SUM(oi.line_total), 2) AS total_revenue,
        ROUND(SUM(oi.line_profit), 2) AS total_profit,
        ROUND(AVG(oi.discount) * 100, 2) AS avg_discount_pct,
        ROUND(SUM(oi.line_total) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT
    year_month,
    total_orders,
    active_customers,
    total_units_sold,
    total_revenue,
    total_profit,
    ROUND((total_profit / total_revenue) * 100, 2) AS profit_margin_pct,
    avg_discount_pct,
    average_order_value,
    LAG(total_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(
        ((total_revenue - LAG(total_revenue, 1) OVER (ORDER BY year_month)) / 
        NULLIF(LAG(total_revenue, 1) OVER (ORDER BY year_month), 0)) * 100, 
        2
    ) AS mom_revenue_growth_pct,
    LAG(total_profit, 1) OVER (ORDER BY year_month) AS prev_month_profit,
    ROUND(
        ((total_profit - LAG(total_profit, 1) OVER (ORDER BY year_month)) / 
        NULLIF(LAG(total_profit, 1) OVER (ORDER BY year_month), 0)) * 100, 
        2
    ) AS mom_profit_growth_pct
FROM monthly_agg;

-- 3. Customer RFM Base Metrics View
CREATE VIEW IF NOT EXISTS v_customer_rfm_base AS
WITH customer_orders AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.city,
        c.region,
        c.segment,
        c.signup_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(oi.line_total), 2) AS monetary,
        ROUND(SUM(oi.line_profit), 2) AS total_profit,
        ROUND(AVG(oi.line_total), 2) AS avg_order_item_val,
        ROUND(AVG(oi.discount), 4) AS avg_discount_rate,
        COUNT(DISTINCT p.category_id) AS distinct_categories_bought,
        MAX(o.order_date) AS last_order_date,
        MIN(o.order_date) AS first_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    GROUP BY c.customer_id, c.customer_name, c.city, c.region, c.segment, c.signup_date
)
SELECT
    customer_id,
    customer_name,
    city,
    region,
    segment,
    signup_date,
    frequency,
    COALESCE(monetary, 0.00) AS monetary,
    COALESCE(total_profit, 0.00) AS total_profit,
    ROUND(COALESCE(monetary, 0.00) / NULLIF(frequency, 0), 2) AS average_order_value,
    COALESCE(avg_discount_rate, 0.00) AS avg_discount_rate,
    COALESCE(distinct_categories_bought, 0) AS category_diversity,
    first_order_date,
    last_order_date,
    CAST(julianday('2026-08-20') - julianday(COALESCE(last_order_date, signup_date)) AS INTEGER) AS recency_days,
    CAST(julianday('2026-08-20') - julianday(signup_date) AS INTEGER) AS tenure_days
FROM customer_orders;

-- 4. Product Profitability and Performance Matrix
CREATE VIEW IF NOT EXISTS v_product_profitability_matrix AS
SELECT
    p.product_id,
    p.product_name,
    cat.category_name,
    p.price,
    p.cost,
    ROUND((p.price - p.cost), 2) AS unit_margin,
    ROUND(((p.price - p.cost) / p.price) * 100, 2) AS gross_margin_pct,
    COUNT(DISTINCT oi.order_id) AS total_orders_present,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(SUM(oi.line_profit), 2) AS total_profit,
    ROUND(AVG(oi.discount) * 100, 2) AS avg_discount_pct,
    CASE
        WHEN SUM(oi.line_profit) > 50000 AND (SUM(oi.line_profit) / SUM(oi.line_total)) >= 0.40 THEN 'Star Performer'
        WHEN SUM(oi.line_total) > 100000 AND (SUM(oi.line_profit) / SUM(oi.line_total)) < 0.35 THEN 'High Volume Low Margin'
        WHEN (SUM(oi.line_profit) / SUM(oi.line_total)) >= 0.50 THEN 'High Margin Niche'
        ELSE 'Standard'
    END AS product_quadrant
FROM products p
JOIN categories cat ON p.category_id = cat.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, cat.category_name, p.price, p.cost;

-- 5. Regional Summary View
CREATE VIEW IF NOT EXISTS v_regional_summary AS
SELECT
    o.region,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(SUM(oi.line_profit), 2) AS total_profit,
    ROUND((SUM(oi.line_profit) / SUM(oi.line_total)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(oi.line_total) / COUNT(DISTINCT o.order_id), 2) AS aov
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.region;

-- 6. Category Performance Summary View
CREATE VIEW IF NOT EXISTS v_category_summary AS
SELECT
    cat.category_id,
    cat.category_name,
    COUNT(DISTINCT p.product_id) AS product_count,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(SUM(oi.line_profit), 2) AS total_profit,
    ROUND((SUM(oi.line_profit) / SUM(oi.line_total)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(oi.discount) * 100, 2) AS avg_discount_pct
FROM categories cat
JOIN products p ON cat.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY cat.category_id, cat.category_name;
