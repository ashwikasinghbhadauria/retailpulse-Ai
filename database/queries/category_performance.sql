-- ========================================================
-- Query: Category Performance Breakdown
-- ========================================================
SELECT
    category_id,
    category_name,
    product_count,
    total_orders,
    total_units_sold,
    total_revenue,
    total_profit,
    profit_margin_pct,
    avg_discount_pct,
    ROUND((total_revenue / (SELECT SUM(total_revenue) FROM v_category_summary)) * 100, 2) AS revenue_share_pct
FROM v_category_summary
ORDER BY total_revenue DESC;
