# RetailPulse AI — REST API Documentation (v1)

The RetailPulse AI backend provides high-performance, strictly typed REST API endpoints built with **FastAPI** and **Pydantic v2**.

Base URL: `http://localhost:8000/api` or `http://localhost:8000/api/v1`  
Interactive Swagger UI: `http://localhost:8000/docs`  
ReDoc UI: `http://localhost:8000/redoc`

---

## Endpoint Reference

### 1. System & Health
- **`GET /api/health`**
  - **Description**: Verifies service status and database connectivity.
  - **Response (200 OK)**:
    ```json
    {
      "status": "healthy",
      "environment": "development",
      "database_connected": true,
      "version": "1.0.0"
    }
    ```

### 2. Executive Overview
- **`GET /api/dashboard/summary`**
  - **Description**: Returns top-line enterprise KPIs and latest monthly performance.
  - **Response (200 OK)**:
    ```json
    {
      "total_revenue": 18767692.85,
      "total_profit": 9614747.75,
      "overall_margin_pct": 51.23,
      "total_orders": 57418,
      "total_customers": 12000,
      "active_customers": 12000,
      "average_order_value": 326.86,
      "latest_month": "2026-08",
      "latest_monthly_revenue": 341052.12,
      "latest_monthly_profit": 174820.50,
      "mom_revenue_growth_pct": 4.12,
      "mom_profit_growth_pct": 3.85
    }
    ```

### 3. Sales Analytics
- **`GET /api/sales/trends`**
  - **Query Params**: `start_date` (optional, `YYYY-MM`), `end_date` (optional, `YYYY-MM`)
  - **Description**: Returns monthly revenue, profit, units sold, and MoM growth rate.

- **`GET /api/sales/regions`**
  - **Description**: Returns territorial breakdowns with revenue share, gross margin %, and AOV.

- **`GET /api/sales/categories`**
  - **Description**: Returns category level volumes, gross profit, margin %, and average discount rates.

### 4. Merchandising & Product Intelligence
- **`GET /api/products/top`**
  - **Query Params**: `limit` (default 10, max 50), `sort_by` (`revenue` | `profit` | `units`)
  - **Description**: Ranked listing of top-performing SKUs.

- **`GET /api/products/underperforming`**
  - **Query Params**: `limit` (default 10)
  - **Description**: Identifies products with lowest profit margins or high discount erosion.

### 5. Customer Analytics & Churn
- **`GET /api/customers/segments`**
  - **Description**: Returns K-Means RFM clustering results with optimal \(k\) silhouette score.

- **`GET /api/customers/churn`**
  - **Description**: Returns churn classifier benchmarks (ROC-AUC, Precision, Recall, F1), risk bands, and top at-risk VIP accounts.

### 6. Demand Forecasting
- **`GET /api/forecast`**
  - **Description**: Returns 6-month projected revenue timeline with 90% confidence bands and category trajectories.

### 7. Prescriptive Recommendations
- **`GET /api/recommendations`**
  - **Description**: Prioritized strategic recommendations grounded in empirical data.

### 8. Generative AI Business Analyst
- **`POST /api/ai/ask`**
  - **Request Body**:
    ```json
    {
      "question": "Which category is most profitable?"
    }
    ```
  - **Response (200 OK)**:
    ```json
    {
      "question": "Which category is most profitable?",
      "tool_called": "get_category_profit",
      "answer": "'Electronics' is the most profitable category with $3.45M in gross profit...",
      "evidence": { "top_category": "Electronics", "top_profit": "$3,450,120.50" },
      "interpretation": "Category demand is concentrated in Electronics with strong pricing power.",
      "recommendation": "Maintain adequate inventory depth and preserve current pricing tiers.",
      "caveat": "Category margins account for COGS and discounts."
    }
    ```
