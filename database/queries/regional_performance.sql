-- ========================================================
-- Query: Regional Performance Breakdown
-- ========================================================
SELECT
    region,
    total_orders,
    total_customers,
    total_units_sold,
    total_revenue,
    total_profit,
    profit_margin_pct,
    aov,
    ROUND((total_revenue / (SELECT SUM(total_revenue) FROM v_regional_summary)) * 100, 2) AS revenue_share_pct
FROM v_regional_summary
ORDER BY total_revenue DESC;
