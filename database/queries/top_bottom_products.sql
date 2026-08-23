-- ========================================================
-- Query: Top 10 by Revenue & Bottom 10 Products by Margin
-- ========================================================

-- Top 10 Products by Revenue
SELECT
    product_id,
    product_name,
    category_name,
    price,
    cost,
    total_units_sold,
    total_revenue,
    total_profit,
    gross_margin_pct,
    product_quadrant
FROM v_product_profitability_matrix
ORDER BY total_revenue DESC
LIMIT 10;

-- Bottom 10 Products by Gross Margin % (Underperforming / Margin Erosion)
SELECT
    product_id,
    product_name,
    category_name,
    price,
    cost,
    total_units_sold,
    total_revenue,
    total_profit,
    gross_margin_pct,
    avg_discount_pct,
    product_quadrant
FROM v_product_profitability_matrix
ORDER BY gross_margin_pct ASC, total_revenue DESC
LIMIT 10;
