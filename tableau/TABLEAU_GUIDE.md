# Tableau Storybook & Analytics Guide — RetailPulse AI

This guide documents the complete reproduction steps for creating the **RetailPulse AI 7-Story Analytics Dashboard** in Tableau Desktop / Tableau Public.

---

## 1. Data Source Setup

1. Open **Tableau Desktop**.
2. Connect to **Text file** -> Select `data/processed/tableau_retail_master_extract.csv`.
3. In Data Source view:
   - Ensure `Order Date` is recognized as a `Date` data type.
   - Verify `Revenue`, `Profit`, `Quantity`, `Unit Price`, and `Discount` are numeric measures.

---

## 2. Calculated Fields & Level of Detail (LOD) Expressions

Create the following Calculated Fields in Tableau:

### Financial & Margin Calculations
```tableau
// 1. Gross Profit Margin Ratio
[Gross Profit Margin] = 
SUM([Profit]) / SUM([Revenue])

// 2. Average Order Value (AOV)
[Average Order Value] = 
SUM([Revenue]) / COUNTD([Order ID])

// 3. Discount Amount ($)
[Discount Amount] = 
SUM(([Unit Price] * [Quantity]) * [Discount])
```

### Advanced LOD Expressions (Fixed & Exclude)
```tableau
// 4. Customer Lifetime Value (CLV)
[Customer Lifetime Value] = 
{ FIXED [Customer ID] : SUM([Revenue]) }

// 5. Customer Total Orders
[Customer Order Count] = 
{ FIXED [Customer ID] : COUNTD([Order ID]) }

// 6. Customer Last Purchase Date
[Customer Last Order Date] = 
{ FIXED [Customer ID] : MAX([Order Date]) }

// 7. Customer Recency Days
[Customer Recency Days] = 
DATEDIFF('day', [Customer Last Order Date], TODAY())

// 8. Category Overall Revenue (for % of Total)
[Category Overall Revenue] = 
{ EXCLUDE [Product Name] : SUM([Revenue]) }
```

### Segmentation & Churn Logic
```tableau
// 9. Customer RFM Tier
[Customer RFM Tier] = 
IF [Customer Lifetime Value] >= 3000 AND [Customer Order Count] >= 6 THEN "Champions / High Value"
ELSEIF [Customer Recency Days] > 180 THEN "At Risk / Inactive"
ELSEIF [Customer Order Count] >= 3 THEN "Loyal Regulars"
ELSE "Occasional Buyers"
END

// 10. Churn Risk Indicator
[Churn Risk Color] = 
IF [Churn Risk Band] = "High Risk (>70%)" THEN "Red"
ELSEIF [Churn Risk Band] = "Medium Risk (30-70%)" THEN "Orange"
ELSE "Green"
END
```

---

## 3. 7-Dashboard Story Architecture

### Story Point 1: Executive Overview
- **Visuals**: KPI summary banners (Revenue, Profit, Margin %, Orders, Customers), Monthly Area Chart (Revenue & Profit dual-axis), Regional map / shape breakdown.

### Story Point 2: Sales Trends & Seasonality
- **Visuals**: Continuous monthly revenue trend with reference lines, Month-over-Month growth rate bar chart, Monthly seasonality heatmap matrix (Month on Columns, Year on Rows, Color by Revenue).

### Story Point 3: Regional Geospatial Performance
- **Visuals**: Filled map of US states / regions colored by Gross Profit Margin %, Side bar chart of revenue and AOV by region with interactive region filter.

### Story Point 4: Customer RFM Segmentation
- **Visuals**: Scatter plot (`Customer Recency Days` on X-axis, `Customer Lifetime Value` on Y-axis, Color by `Customer RFM Tier`), Segment customer count vs revenue contribution bullet chart.

### Story Point 5: Product Profitability Matrix
- **Visuals**: 4-Quadrant Scatter plot (`Revenue` on X-axis, `Gross Profit Margin` on Y-axis, Size by `Quantity`, Color by `Category Name`). Top 10 SKUs bar chart and bottom 10 margin drag table.

### Story Point 6: Predictive Demand Forecasting
- **Visuals**: Tableau built-in Exponential Smoothing Forecast (6-month horizon, 90% prediction intervals), Forecast vs Target comparison card.

### Story Point 7: Strategic Prescriptive Directives
- **Visuals**: Executive summary card layout highlighting the 5 key prescriptive directives (VIP Win-Back, Category Discount Caps, Q4 Inventory Buffers, SKU Rationalization, and Regional Marketing Re-allocation).
