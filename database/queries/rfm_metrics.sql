-- ========================================================
-- Query: Customer RFM and Lifetime Value Metrics
-- ========================================================
SELECT
    customer_id,
    customer_name,
    city,
    region,
    segment,
    recency_days,
    frequency,
    monetary,
    total_profit,
    average_order_value,
    avg_discount_rate,
    category_diversity,
    tenure_days,
    CASE
        WHEN frequency >= 8 AND monetary >= 3000 AND recency_days <= 60 THEN 'High Value / Champion'
        WHEN frequency >= 4 AND recency_days <= 90 THEN 'Loyal Regular'
        WHEN frequency >= 2 AND recency_days > 180 THEN 'At Risk / Inactive'
        WHEN frequency = 1 AND recency_days <= 90 THEN 'New Customer'
        ELSE 'Occasional Buyer'
    END AS heuristic_segment
FROM v_customer_rfm_base
ORDER BY monetary DESC;
