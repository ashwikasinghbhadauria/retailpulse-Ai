# RetailPulse AI — Data Dictionary & Metric Definitions

This data dictionary defines all core data fields, engineered features, and derived business metrics utilized throughout RetailPulse AI.

---

## 1. Primary Financial & Operational Metrics

| Metric | Formula / Calculation | Business Definition |
| :--- | :--- | :--- |
| **Total Revenue** | `SUM(line_total)` | Total monetary revenue generated across all completed line items after promotional discounts. |
| **Total COGS** | `SUM(quantity * product.cost)` | Cost of Goods Sold; total wholesale manufacturing/procurement cost of units sold. |
| **Gross Profit** | `Total Revenue - Total COGS` | Net financial gain generated from sales before operational overhead. |
| **Gross Profit Margin %** | `(Gross Profit / Total Revenue) * 100` | Percentage of top-line revenue retained as gross profit. Measures enterprise pricing power. |
| **Average Order Value (AOV)**| `Total Revenue / Total Orders` | Average dollar amount spent per customer order transaction. |
| **Average Revenue Per User (ARPU)** | `Total Revenue / Total Customers` | Average monetary spend per unique registered customer. |
| **Average Discount %** | `AVG(discount) * 100` | Mean percentage markdown granted on sold items. |
| **MoM Revenue Growth %** | `((Rev_t - Rev_{t-1}) / Rev_{t-1}) * 100` | Month-over-month percentage growth in total revenue. |

---

## 2. Customer RFM & Behavioral Features

| Feature | Data Type | Description |
| :--- | :--- | :--- |
| **Recency (`recency_days`)** | Integer | Number of days elapsed between the analysis anchor date (2026-08-20) and the customer's most recent order date. |
| **Frequency (`frequency`)** | Integer | Total count of distinct orders completed by the customer. |
| **Monetary (`monetary`)** | Float | Cumulative historical spending (gross revenue) by the customer. |
| **Tenure (`tenure_days`)** | Integer | Number of days elapsed between customer signup date and current date. |
| **Purchase Cadence (`purchase_cadence_days`)** | Float | `tenure_days / frequency`. Average number of days between successive customer orders. |
| **Category Diversity** | Integer | Count of distinct product categories purchased by the customer. |
| **Average Discount Usage** | Float | Mean discount percentage applied across the customer's order history. |

---

## 3. Machine Learning & Predictive Metrics

| Metric / Term | Description |
| :--- | :--- |
| **Churn Business Definition** | A customer who registered >= 60 days ago, made at least 1 order, but has had zero purchase activity in the past 180 days (`recency_days > 180`). |
| **Churn Probability** | Continuous probability score `P(Churn=1)` output by the champion classifier (`[0.0, 1.0]`). |
| **Risk Bands** | - **Low Risk**: `P < 0.30`<br>- **Medium Risk**: `0.30 <= P <= 0.70`<br>- **High Risk**: `P > 0.70` |
| **Demand Forecast Horizon** | Multi-step 6-month projected forward revenue. |
| **Prediction Uncertainty Band** | 90% Confidence Interval calculated via empirical error residual standard deviation \(\pm 1.645 \cdot \sigma_t\). |
| **MAPE** | Mean Absolute Percentage Error: \(\frac{1}{n} \sum \left| \frac{y - \hat{y}}{y} \right| \times 100\). Primary time-series accuracy benchmark. |
