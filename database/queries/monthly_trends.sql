-- ========================================================
-- Query: Monthly Sales and Profit Trends with MoM Growth
-- ========================================================
SELECT
    year_month,
    total_orders,
    active_customers,
    total_units_sold,
    total_revenue,
    total_profit,
    profit_margin_pct,
    avg_discount_pct,
    average_order_value,
    COALESCE(mom_revenue_growth_pct, 0.00) AS mom_revenue_growth_pct,
    COALESCE(mom_profit_growth_pct, 0.00) AS mom_profit_growth_pct
FROM v_monthly_sales_summary
ORDER BY year_month ASC;
