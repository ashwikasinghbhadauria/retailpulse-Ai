# Power BI Build Guide — RetailPulse AI

This document provides step-by-step instructions to connect, model, and build the 5-page enterprise **RetailPulse AI** report in Microsoft Power BI Desktop.

---

## 1. Data Source Connection & Ingestion

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV** (or connect via PostgreSQL if running on a database server).
3. Import the 3 star-schema tables from `data/processed/`:
   - `powerbi_fact_sales.csv` (Rename table to `fact_sales`)
   - `powerbi_dim_customers.csv` (Rename table to `dim_customers`)
   - `powerbi_dim_date.csv` (Rename table to `dim_date`)
4. In Power Query Editor:
   - Verify `fact_sales[order_date]` is parsed as `Date`.
   - Verify `dim_date[Date]` is parsed as `Date`.
   - Set `dim_date` as the **Official Date Table** in Model view.
   - Click **Close & Apply**.

---

## 2. Star Schema Data Model Relationships

Navigate to the **Model View** and configure the following 1-to-Many single-direction relationships:

```
+-----------------------------------+
|          dim_customers            |
| - customer_id (PK)                |
+-----------------------------------+
                  | (1)
                  |
                  | (*)
+-----------------------------------+          +-----------------------------------+
|            fact_sales             | (*)------|             dim_date              |
| - customer_id (FK)                |          | - Date (PK)                       |
| - order_date (FK)                 |          +-----------------------------------+
| - product_id (FK)                 |
+-----------------------------------+
```

- `dim_customers[customer_id]` `1` <---> `*` `fact_sales[customer_id]` (Cross filter: Single)
- `dim_date[Date]` `1` <---> `*` `fact_sales[order_date]` (Cross filter: Single)

---

## 3. DAX Measures Setup

1. In Power BI, create a dedicated table named `_Measures`.
2. Open `powerbi/DAX_MEASURES.dax` and copy all 30+ measures into the `_Measures` table.

---

## 4. Report Page Design Specifications

### Page 1: Executive Overview
- **Top KPIs**: Card visuals for `[Total Revenue]`, `[Total Gross Profit]`, `[Gross Profit Margin %]`, `[Total Orders]`, `[Total Distinct Customers]`, `[Average Order Value]`.
- **Main Visual**: Area chart of `dim_date[YearMonth]` on X-axis, `[Total Revenue]` and `[Total Gross Profit]` on Y-axis.
- **Donut Visual**: `fact_sales[region]` on Legend, `[Total Revenue]` on Values.
- **Bar Visual**: `fact_sales[category_name]` on Y-axis, `[Total Revenue]` and `[Total Gross Profit]` on X-axis.
- **Slicers**: Date range slider (`dim_date[Date]`), Region dropdown (`fact_sales[region]`).

### Page 2: Sales Performance & Trends
- **Line & Clustered Column Chart**: `dim_date[YearMonth]` on X-axis, `[Total Revenue]` as Columns, `[MoM Revenue Growth %]` as Line.
- **Matrix Visual**: Rows = `fact_sales[region]`, Columns = `fact_sales[category_name]`, Values = `[Total Revenue]`, `[Gross Profit Margin %]`.
- **Ledger Table**: Columns = `YearMonth`, `Total Orders`, `Total Units Sold`, `Total Revenue`, `Total Gross Profit`, `MoM Growth %`, `AOV`.

### Page 3: Customer Intelligence & RFM
- **Bar Chart**: `dim_customers[heuristic_segment]` on Y-axis, `[Total Distinct Customers]` and `[High Value Champions Revenue]` on Values.
- **Churn Risk Donut**: Legend = `dim_customers[churn_risk_band]`, Values = `Count of Customers`.
- **VIP At-Risk Grid**: Filtered table where `churn_risk_band = "High Risk (>70%)"` sorted descending by `[monetary]`.

### Page 4: Product Performance & Margin Matrix
- **Scatter Plot**: X-axis = `[Total Revenue]`, Y-axis = `[Gross Profit Margin %]`, Bubble Size = `[Total Units Sold]`, Legend = `fact_sales[category_name]`.
- **Top 10 SKUs Bar Chart**: `fact_sales[product_name]` on Y-axis, `[Total Revenue]` on X-axis (Filter Top 10 by `[Total Revenue]`).
- **Underperforming Table**: Bottom 10 SKUs by `[Gross Profit Margin %]` showing discount percentage and unit cost.

### Page 5: Demand Forecasting & Target Variance
- **Forecasting Line Chart**: Historical `[Total Revenue]` with built-in Power BI Analytics Forecast tool (Horizon = 6 Months, Confidence Interval = 90%).
- **Variance Gauge**: Actual `[Total Revenue]` vs `[Target Monthly Revenue]` with color thresholds.
