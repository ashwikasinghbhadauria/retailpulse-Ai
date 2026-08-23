"""
FastAPI Backend Integration & Endpoint Tests
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "version" in data

def test_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_revenue"] > 0
    assert data["total_profit"] > 0
    assert data["total_orders"] > 0
    assert data["total_customers"] > 0
    assert 0 <= data["overall_margin_pct"] <= 100

def test_sales_trends():
    response = client.get("/api/sales/trends")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    first = data[0]
    assert "year_month" in first
    assert "total_revenue" in first

def test_regional_breakdown():
    response = client.get("/api/sales/regions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5 # 5 regions
    regions = [r["region"] for r in data]
    assert "West" in regions
    assert "East" in regions

def test_category_breakdown():
    response = client.get("/api/sales/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5 # 5 categories

def test_top_products():
    response = client.get("/api/products/top?limit=10&sort_by=revenue")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert data[0]["total_revenue"] >= data[-1]["total_revenue"]

def test_underperforming_products():
    response = client.get("/api/products/underperforming?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

def test_customer_segments():
    response = client.get("/api/customers/segments")
    assert response.status_code == 200
    data = response.json()
    assert data["optimal_k"] in [3, 4, 5]
    assert len(data["segments"]) == data["optimal_k"]
    assert data["total_segmented_customers"] > 0

def test_customer_churn():
    response = client.get("/api/customers/churn")
    assert response.status_code == 200
    data = response.json()
    assert data["champion_model"] in ["Logistic Regression", "Random Forest", "Gradient Boosting"]
    assert data["champion_roc_auc"] > 0.5
    assert len(data["model_comparisons"]) == 3
    assert len(data["risk_band_distribution"]) == 3

def test_demand_forecast():
    response = client.get("/api/forecast")
    assert response.status_code == 200
    data = response.json()
    assert data["forecast_horizon_months"] == 6
    assert len(data["forecast_timeline"]) > 0
    assert data["next_quarter_projected_revenue"] > 0

def test_recommendations():
    response = client.get("/api/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert "title" in data[0]
    assert "recommended_action" in data[0]

def test_ai_business_analyst_questions():
    questions = [
        "Which category is most profitable?",
        "Which region is underperforming?",
        "What is our churn risk distribution?",
        "What will future sales look like?",
        "What should management focus on?"
    ]
    for q in questions:
        response = client.post("/api/ai/ask", json={"question": q})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert len(data["answer"]) > 10
        assert "evidence" in data
        assert "interpretation" in data
        assert "recommendation" in data
        assert "tool_called" in data
