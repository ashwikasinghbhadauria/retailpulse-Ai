# RetailPulse AI — System Architecture & Technical Specifications

RetailPulse AI is built as a multi-tier, enterprise-ready retail intelligence platform combining real-time transactional data engineering, statistical analytics, machine learning predictive models, prescriptive heuristic systems, and a strictly controlled tool-calling Generative AI conversational layer.

```
+-----------------------------------------------------------------------------------------------+
|                                    PRESENTATION LAYER                                         |
|                                                                                               |
|   +------------------------------------+             +------------------------------------+   |
|   |       React 18 + TypeScript        |             |       Power BI & Tableau BI        |   |
|   |  - Vite, TailwindCSS, Lucide Icons |             |  - 30+ Production DAX Measures     |   |
|   |  - Recharts Visualizations         |             |  - Star Schema Data Model          |   |
|   |  - 6 Analytics & AI Portals        |             |  - 7-Story Dashboard Reproduction  |   |
|   +------------------------------------+             +------------------------------------+   |
+-----------------------------------------------------------------------------------------------+
                                                |
                                                | HTTP / REST (JSON)
                                                v
+-----------------------------------------------------------------------------------------------+
|                                    APPLICATION & API LAYER                                    |
|                                                                                               |
|   +---------------------------------------------------------------------------------------+   |
|   |                                FastAPI Gateway (v1)                                   |   |
|   |   - Pydantic v2 Request/Response Validation                                           |   |
|   |   - Global Structured Exception Handling & Performance Logging                        |   |
|   |   - Interactive OpenAPI/Swagger Documentation (/docs, /redoc)                         |   |
|   +---------------------------------------------------------------------------------------+   |
|                                                |                                              |
|            +-----------------------------------+-----------------------------------+          |
|            |                                   |                                   |          |
|            v                                   v                                   v          |
|   +-------------------+               +-------------------+               +---------------+   |
|   | Analytics Engine  |               |    ML Services    |               |  GenAI Agent  |   |
|   | - SQL Views & CTEs|               | - RFM K-Means     |               | - Tool-Calling|   |
|   | - Window Funcs    |               | - Churn Classifier|               | - Safe SQL    |   |
|   | - Descriptive KPIs|               | - Demand Forecast |               | - 5-Part Synth|   |
|   | - Diagnostics     |               | - Model Store     |               | - Fallback    |   |
|   +-------------------+               +-------------------+               +---------------+   |
+-----------------------------------------------------------------------------------------------+
                                                |
                                                | SQLAlchemy ORM / Native Connection Pools
                                                v
+-----------------------------------------------------------------------------------------------+
|                                    DATA & PERSISTENCE LAYER                                   |
|                                                                                               |
|   +---------------------------------------------------------------------------------------+   |
|   |                       Normalized PostgreSQL / SQLite Warehouse (3NF)                  |   |
|   |   - categories, customers, products, orders, order_items                              |   |
|   |   - High-performance composite indexes on regions, dates, customers, products         |   |
|   |   - Optimized analytical views (v_monthly_sales_summary, v_customer_rfm_base, etc.)   |   |
|   +---------------------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------------------+
```

---

## Component Deep Dive

### 1. Data Engineering & Persistence
- **Normalized 3NF Schema**: Ensures transactional consistency without anomalies. Foreign keys maintain referential integrity.
- **Analytical Views**: Pre-aggregates line items, computing costs, revenues, discounts, margins, and cohort recencies.
- **Dual Support**: Seamlessly executes against enterprise PostgreSQL or zero-config local SQLite.

### 2. Analytics & Diagnostic Engine
- **Window Functions**: Leverages `LAG() OVER (ORDER BY year_month)` for exact month-over-month revenue and profit growth.
- **Automated Diagnostics**: Evaluates discount drag, category margin compression, and regional margin spreads.

### 3. Machine Learning Suite
- **Customer Segmentation**: Log-transforms skewed monetary and recency variables, standardizes features, evaluates silhouette coefficients across clusters, and labels clusters into business personas.
- **Churn Prediction**: Compares Logistic Regression, Random Forest, and Gradient Boosting on ROC-AUC, Recall, and F1. Stratified 75/25 split prevents data leakage.
- **Demand Forecasting**: Autoregressive multi-step lag model incorporating rolling statistics and cyclical trigonometric seasonality to predict a 6-month horizon with 90% confidence bands.

### 4. Controlled GenAI Business Analyst
- **Zero-Arbitrary SQL Security**: Eliminates prompt injection risks. The LLM has zero direct database credentials.
- **Tool-Calling Architecture**: The LLM routes user intents exclusively to authorized, schema-validated Python/SQL tools.
- **Structured 5-Part Response**: Every answer is systematically broken into Answer, Evidence, Interpretation, Recommendation, and Caveat.
