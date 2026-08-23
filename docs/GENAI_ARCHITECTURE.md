# RetailPulse AI — Generative AI & Tool-Calling Architecture

This document describes the security, tool-calling pipeline, prompt engineering, and structured synthesis architecture powering the **AI Business Analyst** in RetailPulse AI.

---

## 1. Zero-Arbitrary SQL Security Model

A critical vulnerability in naive GenAI analytics applications is allowing an LLM to generate and execute freeform SQL queries directly against a database. This introduces catastrophic risks:
- SQL injection / prompt injection
- Accidental denial-of-service via unindexed Cartesian joins
- Hallucinated column names or erroneous calculations
- Exposing raw sensitive database connection strings

### RetailPulse AI Controlled Architecture
```
[User Question]
       │
       ▼
[OpenAI Function Calling Gateway]
       │
       ├─► Validates user intent against 10 Authorized Tool Schemas
       │
       ▼
[Registered Python / SQL Tool Invocation] (get_category_profit, get_churn_summary, etc.)
       │
       ├─► Executes parameterized, index-optimized analytical views
       │
       ▼
[Structured Verification & Synthesis]
       │
       ▼
[Systematic 5-Part Structured Response]
  ├─ 1. Answer (Concise executive response)
  ├─ 2. Evidence (Verified numerical facts extracted from tools)
  ├─ 3. Interpretation (Analytical business meaning)
  ├─ 4. Recommendation (Prescriptive management action)
  └─ 5. Caveat (Assumptions & limitations)
```

---

## 2. Authorized Analytical Tool Registry

| Tool Function | Description | Parameters |
| :--- | :--- | :--- |
| `get_executive_metrics` | Retrieves enterprise total revenue, gross profit, margin %, orders, and AOV. | None |
| `get_sales_trend` | Retrieves monthly historical sales, revenue, and MoM growth trajectories. | `start_date`, `end_date` |
| `get_category_profit` | Computes revenue, profit, margin %, and average discounts per category. | None |
| `get_region_performance` | Calculates regional sales volume, revenue share, margin %, and AOV. | None |
| `get_customer_segments` | Retrieves K-Means RFM clusters and behavioral segment statistics. | None |
| `get_top_products` | Retrieves top performing products sorted by revenue, profit, or units. | `limit`, `sort_by` |
| `get_underperforming_products` | Identifies products with margin compression or excessive discounting. | `limit` |
| `get_churn_summary` | Fetches churn model benchmarks, population risk bands, and top at-risk VIPs. | None |
| `get_forecast` | Returns 6-month demand forecast timeline and 90% confidence bands. | None |
| `get_prescriptive_recommendations`| Returns prioritized strategic business recommendations. | None |

---

## 3. High-Availability Deterministic Fallback Engine

If the OpenAI API key is unset or external network connectivity is unavailable, RetailPulse AI executes an internal NLP intent parser and deterministic analytics synthesizer. This guarantees that:
- The platform never crashes or returns HTTP 500 errors.
- Real-time numerical metrics from the data warehouse are synthesized into the exact same 5-part structured JSON schema.
