from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Health Schema
class HealthResponse(BaseModel):
    status: str = "healthy"
    environment: str
    database_connected: bool
    version: str = "1.0.0"

# Executive Summary Schema
class ExecutiveSummaryResponse(BaseModel):
    total_revenue: float
    total_profit: float
    overall_margin_pct: float
    total_orders: int
    total_customers: int
    active_customers: int
    average_order_value: float
    latest_month: str
    latest_monthly_revenue: float
    latest_monthly_profit: float
    mom_revenue_growth_pct: float
    mom_profit_growth_pct: float

# Sales Trends Schema
class MonthlyTrendItem(BaseModel):
    year_month: str
    total_orders: int
    active_customers: int
    total_units_sold: int
    total_revenue: float
    total_profit: float
    profit_margin_pct: float
    avg_discount_pct: float
    average_order_value: float
    mom_revenue_growth_pct: float
    mom_profit_growth_pct: float

# Regional Performance Schema
class RegionalItem(BaseModel):
    region: str
    total_orders: int
    total_customers: int
    total_units_sold: int
    total_revenue: float
    total_profit: float
    profit_margin_pct: float
    revenue_share_pct: float
    average_order_value: float
    avg_discount_pct: float

# Category Performance Schema
class CategoryItem(BaseModel):
    category_id: str
    category_name: str
    product_count: int
    total_orders: int
    total_units_sold: int
    total_revenue: float
    total_profit: float
    profit_margin_pct: float
    revenue_share_pct: float
    avg_discount_pct: float

# Product Performance Schema
class ProductItem(BaseModel):
    product_id: str
    product_name: str
    category_name: str
    price: float
    total_orders: int
    total_units_sold: int
    total_revenue: float
    total_profit: float
    gross_margin_pct: float
    avg_discount_pct: float
    risk_flag: Optional[str] = None

# Customer Segmentation Schema
class SegmentItem(BaseModel):
    cluster_id: int
    segment_name: str
    customer_count: int
    customer_share_pct: float
    total_revenue: float
    total_profit: float
    revenue_share_pct: float
    avg_recency_days: float
    avg_frequency: float
    avg_monetary: float
    avg_order_value: float

class CustomerSegmentsResponse(BaseModel):
    optimal_k: int
    best_silhouette_score: float
    all_evaluated_scores: Dict[str, float]
    total_segmented_customers: int
    segments: List[SegmentItem]

# Customer Churn Schema
class ChurnModelComparison(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: Dict[str, int]

class RiskBandItem(BaseModel):
    risk_band: str
    customer_count: int
    share_pct: float

class AtRiskVIPCustomer(BaseModel):
    customer_id: str
    customer_name: str
    region: str
    segment: str
    total_spend: float
    total_orders: int
    recency_days: int
    churn_probability: float
    risk_band: str

class CustomerChurnResponse(BaseModel):
    champion_model: str
    champion_roc_auc: float
    business_definition: str
    total_analyzed_customers: int
    actual_churn_rate_pct: float
    model_comparisons: List[ChurnModelComparison]
    feature_importances: List[Dict[str, Any]]
    risk_band_distribution: List[RiskBandItem]
    top_at_risk_vip_customers: List[AtRiskVIPCustomer]

# Demand Forecasting Schema
class ForecastTimelinePoint(BaseModel):
    year_month: str
    actual_revenue: Optional[float] = None
    predicted_revenue: Optional[float] = None
    lower_bound_90ci: Optional[float] = None
    upper_bound_90ci: Optional[float] = None
    is_forecast: bool

class DemandForecastResponse(BaseModel):
    model_architecture: str
    validation_metrics: Dict[str, float]
    forecast_horizon_months: int
    forecast_timeline: List[ForecastTimelinePoint]
    next_quarter_projected_revenue: float
    category_forecasts: List[Dict[str, Any]]

# Business Recommendation Schema
class RecommendationItem(BaseModel):
    id: str
    category: str
    priority: str
    effort: str
    title: str
    finding: str
    recommended_action: str
    expected_impact: str

# AI Business Analyst Schemas
class AIQuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=1000, description="Natural language question about business analytics")

class AIAnswerResponse(BaseModel):
    question: str
    tool_called: str
    answer: str
    evidence: Dict[str, Any]
    interpretation: str
    recommendation: str
    caveat: str
