# RetailPulse AI — Autonomous Retail Intelligence & Predictive Analytics Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2.2-3178C6.svg?style=flat&logo=TypeScript&logoColor=white)](https://www.typescriptlang.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4.1-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4.1-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **RetailPulse AI** is an enterprise-grade retail business intelligence, predictive machine learning, and Generative AI analytics platform. It transforms granular point-of-sale and e-commerce transaction data into descriptive KPIs, diagnostic root-cause insights, predictive ML models, prescriptive directives, and a natural-language conversational AI Business Analyst powered by controlled tool calling.

---

## 1. Executive Summary & Business Vision

Modern multi-channel retail organizations process millions of transactions daily across dispersed territories, product categories, and customer cohorts. Business leaders frequently struggle to answer mission-critical questions in real time:
- *Why did gross margins contract in key product categories?*
- *Which high-value VIP customer accounts are silently drifting toward churn?*
- *What will demand look like next quarter by category, and what inventory buffers are required?*
- *How can non-technical stakeholders interrogate enterprise data without querying databases directly?*

**RetailPulse AI** unifies data warehousing, statistical analytics, machine learning, and LLM tool calling into a single cohesive SaaS intelligence platform.

---

## 2. Platform Architecture

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

## 3. Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend UI/UX** | React 18, TypeScript, Vite, Tailwind CSS, Recharts, Lucide Icons, Axios |
| **Backend REST API** | Python 3.10+, FastAPI, Pydantic v2, Uvicorn, SQLAlchemy |
| **Data Engineering** | Pandas, NumPy, SQL (Window Functions, CTEs, Aggregations), OpenPyXL |
| **Machine Learning** | Scikit-learn (K-Means, Random Forest, Gradient Boosting, Ridge, Logistic Regression), Joblib |
| **Generative AI** | OpenAI API (GPT-4o-mini), Function Calling, Structured Output Schemas, Safe Deterministic Engine |
| **BI & Analytics** | Power BI (`.dax`, Star Schema Modeling), Tableau (LOD Expressions, Storybook) |
| **Testing & Quality** | Pytest, Pytest-Asyncio, ESLint, TypeScript Compiler (`tsc`) |

---

## 4. Key Application Modules & Features

### 1. Executive Overview
- **Enterprise KPI Cards**: Total Revenue ($18.7M+), Gross Profit ($9.6M+), Profit Margin (51.2%), Orders (57k+), Customers (12k+), AOV ($326.86).
- **Trajectory Visuals**: Dual-area revenue and gross profit curves.
- **Regional & Category Splits**: Geospatial contribution and category revenue/profit shares.
- **Strategic Directives**: Actionable data-grounded prescriptive recommendations.

### 2. Sales Analytics
- **Time-Series Deep Dive**: Month-over-Month (MoM) revenue growth tracking using SQL window functions (`LAG() OVER`).
- **Interactive Filtering**: Filter by year, quarter, or custom text query.
- **Regional & Category Matrix**: Margin vs discount correlation table.
- **Historical Financial Ledger**: Complete chronological ledger of monthly performance.

### 3. Customer Intelligence & RFM Segmentation
- **K-Means Behavioral Clustering**: 4 distinct customer personas (*Champions / High Value*, *Loyal Regulars*, *Potential Growth*, *At Risk / Inactive*).
- **Silhouette Optimization**: Evaluated across \(k=3..5\) to maximize intra-cluster cohesion.
- **Revenue Contribution vs Population Size**: Identifies high-value concentration.
- **High-Risk VIP Customer Watchlist**: Real-time list of top-spending accounts exhibiting >70% churn risk.

### 4. Merchandising & Product Intelligence
- **Assortment Rankings**: Filter by Top Revenue, Top Profit, or Highest Volume SKUs.
- **Margin Erosion Watchlist**: Identifies products with high discount drag or compressed gross margins.
- **Unit Economics**: Granular visibility into list prices, wholesale COGS, and markdown rates.

### 5. ML & Demand Forecasting
- **Autoregressive Demand Regressor**: 6-month forward sales trajectory with 90% confidence uncertainty bands.
- **Holdout Validation Scorecard**: Evaluates MAPE (25.9%), RMSE, and MAE against moving-average baselines.
- **Supervised Churn Leaderboard**: Benchmarks Logistic Regression vs Random Forest (Champion, ROC-AUC: 0.7842) vs Gradient Boosting.
- **Feature Importance Rankings**: Identifies key churn drivers (purchase cadence, recency, tenure, discount usage).

### 6. Generative AI Business Analyst (Controlled Tool Calling)
- **Zero-Arbitrary SQL Security**: Eliminates injection risks. The LLM never writes raw SQL or touches database credentials.
- **Strictly Grounded 5-Part Responses**:
  1. **Answer**: Crisp executive summary.
  2. **Evidence**: Verified numerical facts extracted from tools.
  3. **Interpretation**: Business context and implications.
  4. **Recommendation**: Prescriptive management directives.
  5. **Caveat**: Analytical assumptions and limitations.
- **Interactive Suggested Questions**: Pre-configured executive queries for instant exploration.

---

## 5. Machine Learning Methodology

### Customer Churn Classification
- **Business Definition**: A customer who joined >= 60 days ago, has at least 1 order, and has had zero purchase activity in the past 180 days.
- **Model Comparison**:
  - **Random Forest (Champion)**: ROC-AUC: **0.7842**, Recall: **0.8462**, F1: **0.7728**
  - **Gradient Boosting**: ROC-AUC: 0.7838, Recall: 0.8407, F1: 0.7732
  - **Logistic Regression**: ROC-AUC: 0.7805, Recall: 0.7961, F1: 0.7503
- **Risk Bands**: Low (<30%), Medium (30–70%), High (>70%).

### RFM Segmentation
- **Features**: Recency (days), Frequency (orders), Monetary ($).
- **Preprocessing**: Natural log transformation (`np.log1p`) + `StandardScaler`.
- **Optimal Clusters**: \(k=4\) (Silhouette Score: **0.3302**).

### Demand Forecasting
- **Architecture**: Gradient Boosting Auto-Regressive Regressor.
- **Features**: Lag 1–3, Rolling 3M mean, Linear trend, Cyclical sine/cosine month seasonality.
- **Horizon**: 6 Months with empirical residual confidence intervals.

---

## 6. Power BI & Tableau Deliverables

### Power BI
- **30+ Production DAX Measures**: Located in [`powerbi/DAX_MEASURES.dax`](file:///C:/Users/Ashwika/OneDrive/Desktop/projects%20(Personal)/retailpulse-ai/powerbi/DAX_MEASURES.dax).
- **Star-Schema Datasets**: Pre-exported in `data/processed/powerbi_*.csv`.
- **Build Guide**: Comprehensive step-by-step 5-page report build guide in [`powerbi/POWERBI_BUILD_GUIDE.md`](file:///C:/Users/Ashwika/OneDrive/Desktop/projects%20(Personal)/retailpulse-ai/powerbi/POWERBI_BUILD_GUIDE.md).

### Tableau
- **Calculated Fields & LOD Expressions**: `{FIXED [Customer ID] : SUM([Revenue])}`, Customer Recency, Margin ratios.
- **Extract File**: `data/processed/tableau_retail_master_extract.csv`.
- **Storybook Guide**: 7-sheet story flow in [`tableau/TABLEAU_GUIDE.md`](file:///C:/Users/Ashwika/OneDrive/Desktop/projects%20%28Personal%29/retailpulse-ai/tableau/TABLEAU_GUIDE.md).

---

## 7. Quickstart Setup Guide

### 1. Backend & Analytics Setup
```powershell
# Clone and enter project directory
cd retailpulse-ai

# Install Python requirements
pip install -r requirements.txt

# Configure environment
copy .env.example .env

# Generate realistic synthetic data (12k customers, 57k orders)
python scripts/generate_data.py

# Initialize database schema and bulk load data
python database/init_db.py

# Train ML models (RFM, Churn, Forecasting)
python scripts/train_models.py

# Export Power BI and Tableau datasets
python scripts/export_bi_datasets.py
```

### 2. Run Backend Server
```powershell
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI will be live at `http://localhost:8000/docs`.

### 3. Run Frontend Server
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

### 4. Run Automated Test Suite
```powershell
pytest backend/tests/ -v
```

---

## 8. Repository Structure

```
retailpulse-ai/
├── backend/
│   ├── app/
│   │   ├── analytics/          # Data loader, metrics engine, diagnostics, recommendations
│   │   ├── api/v1/             # REST API routers and endpoints
│   │   ├── core/               # App configuration, database engine & session
│   │   ├── genai/              # OpenAI tool definitions & safe agent orchestrator
│   │   ├── ml/                 # RFM segmentation, Churn classification, Demand forecasting
│   │   ├── models/             # SQLAlchemy ORM database models
│   │   ├── schemas/            # Pydantic v2 request/response models
│   │   └── main.py             # FastAPI entrypoint & middleware
│   └── tests/                  # Pytest automated test suite
├── database/
│   ├── queries/                # Analytical SQL queries (KPIs, MoM, Regional, RFM)
│   ├── schema.sql              # Normalized 3NF PostgreSQL/SQLite schema
│   ├── views.sql               # Production analytical SQL views
│   └── init_db.py              # Database creation & bulk seeding script
├── data/
│   ├── raw/                    # Generated raw transactional CSVs
│   └── processed/              # Processed Power BI & Tableau star-schema extracts
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI cards, sidebar, navbar
│   │   ├── pages/              # 6 Analytics & AI dashboard pages
│   │   ├── services/           # Axios API client
│   │   ├── types/              # TypeScript data interfaces
│   │   ├── App.tsx             # Root router layout
│   │   └── main.tsx            # React DOM entrypoint
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── powerbi/
│   ├── DAX_MEASURES.dax        # 30+ production DAX measures
│   └── POWERBI_BUILD_GUIDE.md  # 5-page report reproduction specification
├── tableau/
│   └── TABLEAU_GUIDE.md        # LOD expressions and 7-story dashboard guide
├── docs/                       # Technical architecture, database, API, ML model card docs
├── scripts/                    # Data generator, training runner, BI exporter
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 9. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
