-- ========================================================
-- Query: Executive Overview KPIs
-- Purpose: Computes primary high-level business metrics across the entire enterprise
-- ========================================================
SELECT
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(SUM(oi.line_profit), 2) AS total_profit,
    ROUND((SUM(oi.line_profit) / SUM(oi.line_total)) * 100, 2) AS overall_profit_margin_pct,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_active_customers,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.line_total) / COUNT(DISTINCT o.order_id), 2) AS average_order_value,
    ROUND(SUM(oi.line_total) / COUNT(DISTINCT o.customer_id), 2) AS average_revenue_per_customer,
    ROUND(AVG(oi.discount) * 100, 2) AS average_discount_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id;
