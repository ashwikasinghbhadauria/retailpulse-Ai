"""
RetailPulse AI — API v1 Router
Exposes all analytical, machine learning, and GenAI endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.schemas.schemas import (
    HealthResponse,
    ExecutiveSummaryResponse,
    MonthlyTrendItem,
    RegionalItem,
    CategoryItem,
    ProductItem,
    CustomerSegmentsResponse,
    CustomerChurnResponse,
    DemandForecastResponse,
    RecommendationItem,
    AIQuestionRequest,
    AIAnswerResponse
)
from backend.app.analytics.metrics import (
    get_executive_summary,
    get_sales_trends,
    get_regional_breakdown,
    get_category_breakdown,
    get_top_products,
    get_underperforming_products
)
from backend.app.analytics.diagnostics import run_diagnostics
from backend.app.analytics.recommendations import generate_business_recommendations
from backend.app.ml.segmentation import CustomerSegmentationEngine
from backend.app.ml.churn import ChurnPredictionEngine
from backend.app.ml.forecasting import DemandForecastingEngine
from backend.app.genai.agent import genai_agent

api_router = APIRouter()

@api_router.get("/health", response_model=HealthResponse, tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """System health check and database connectivity verification."""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "status": "healthy" if db_ok else "degraded",
        "environment": settings.ENVIRONMENT,
        "database_connected": db_ok,
        "version": "1.0.0"
    }

@api_router.get("/dashboard/summary", response_model=ExecutiveSummaryResponse, tags=["Executive"])
def get_dashboard_summary():
    """Returns top-level executive KPIs and latest monthly metrics."""
    return get_executive_summary()

@api_router.get("/sales/trends", response_model=List[MonthlyTrendItem], tags=["Sales"])
def get_sales_trends_endpoint(
    start_date: Optional[str] = Query(None, description="Start date filter (YYYY-MM)"),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM)")
):
    """Returns monthly sales revenue, profit, unit volumes, and MoM growth."""
    return get_sales_trends(start_date=start_date, end_date=end_date)

@api_router.get("/sales/regions", response_model=List[RegionalItem], tags=["Sales"])
def get_regional_sales():
    """Returns regional sales volume, profit margins, and revenue shares."""
    return get_regional_breakdown()

@api_router.get("/sales/categories", response_model=List[CategoryItem], tags=["Sales"])
def get_category_sales():
    """Returns category breakdown with revenue, profit, margin %, and discounts."""
    return get_category_breakdown()

@api_router.get("/products/top", response_model=List[ProductItem], tags=["Products"])
def get_top_performing_products(
    limit: int = Query(10, ge=1, le=50),
    sort_by: str = Query("revenue", pattern="^(revenue|profit|units)$")
):
    """Returns top products ranked by revenue, profit, or units sold."""
    return get_top_products(limit=limit, sort_by=sort_by)

@api_router.get("/products/underperforming", response_model=List[ProductItem], tags=["Products"])
def get_underperforming_products_endpoint(
    limit: int = Query(10, ge=1, le=50)
):
    """Returns products with lowest profit margins or heavy discount erosion."""
    return get_underperforming_products(limit=limit)

@api_router.get("/customers/segments", response_model=CustomerSegmentsResponse, tags=["Customers"])
def get_customer_segments_endpoint():
    """Returns RFM customer clusters with optimal k silhouette evaluation."""
    return CustomerSegmentationEngine.train_and_segment()

@api_router.get("/customers/churn", response_model=CustomerChurnResponse, tags=["Customers"])
def get_customer_churn_endpoint():
    """Returns multi-model churn comparisons, risk distributions, and top at-risk VIPs."""
    return ChurnPredictionEngine.train_and_evaluate()

@api_router.get("/forecast", response_model=DemandForecastResponse, tags=["Forecasting"])
def get_demand_forecast_endpoint():
    """Returns demand forecasting predictions, 90% confidence bands, and category trajectories."""
    return DemandForecastingEngine.generate_forecast()

@api_router.get("/recommendations", response_model=List[RecommendationItem], tags=["Prescriptive"])
def get_recommendations_endpoint():
    """Returns actionable prescriptive business recommendations grounded in data."""
    return generate_business_recommendations()

@api_router.get("/diagnostics", tags=["Diagnostic"])
def get_diagnostics_endpoint():
    """Returns automated anomaly detection and diagnostic findings."""
    return run_diagnostics()

@api_router.post("/ai/ask", response_model=AIAnswerResponse, tags=["AI Business Analyst"])
def ask_ai_analyst(payload: AIQuestionRequest):
    """Conversational AI Business Analyst using controlled tool-calling architecture."""
    try:
        return genai_agent.ask(payload.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Analyst error: {str(e)}")
