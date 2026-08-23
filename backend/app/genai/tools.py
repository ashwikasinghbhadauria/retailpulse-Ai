"""
RetailPulse AI — Safe Analytical Tools for GenAI Business Analyst
Strictly controlled analytical functions. The LLM cannot execute arbitrary SQL.
"""

from typing import Dict, Any, List, Optional
from backend.app.analytics.metrics import (
    get_executive_summary,
    get_sales_trends,
    get_regional_breakdown,
    get_category_breakdown,
    get_top_products,
    get_underperforming_products
)
from backend.app.ml.segmentation import CustomerSegmentationEngine
from backend.app.ml.churn import ChurnPredictionEngine
from backend.app.ml.forecasting import DemandForecastingEngine
from backend.app.analytics.recommendations import generate_business_recommendations

def tool_get_executive_metrics() -> Dict[str, Any]:
    """Retrieves top-level enterprise KPIs (revenue, profit, margin, orders, customers, AOV)."""
    return get_executive_summary()

def tool_get_sales_trend(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves historical monthly sales, revenue, profit, and MoM growth trajectories."""
    return get_sales_trends(start_date=start_date, end_date=end_date)

def tool_get_category_profit() -> List[Dict[str, Any]]:
    """Retrieves revenue, profit, margin %, order counts, and discount levels for each category."""
    return get_category_breakdown()

def tool_get_region_performance() -> List[Dict[str, Any]]:
    """Retrieves regional breakdown including sales volume, revenue share, margin %, and AOV."""
    return get_regional_breakdown()

def tool_get_customer_segments() -> Dict[str, Any]:
    """Retrieves customer segmentation clusters (Champions, Loyal, At-Risk, Occasional) with RFM metrics."""
    return CustomerSegmentationEngine.train_and_segment()

def tool_get_top_products(limit: int = 10, sort_by: str = "revenue") -> List[Dict[str, Any]]:
    """Retrieves top-performing products ranked by revenue or profit."""
    return get_top_products(limit=limit, sort_by=sort_by)

def tool_get_underperforming_products(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves products with low margins, margin compression, or heavy discount erosion."""
    return get_underperforming_products(limit=limit)

def tool_get_churn_summary() -> Dict[str, Any]:
    """Retrieves ML churn model evaluation metrics, customer risk band distributions, and high-risk VIP accounts."""
    return ChurnPredictionEngine.train_and_evaluate()

def tool_get_forecast() -> Dict[str, Any]:
    """Retrieves demand forecasting predictions, confidence intervals, and category trajectories."""
    return DemandForecastingEngine.generate_forecast()

def tool_get_prescriptive_recommendations() -> List[Dict[str, Any]]:
    """Retrieves data-grounded prescriptive recommendations across pricing, retention, and supply chain."""
    return generate_business_recommendations()

# OpenAI Tool Specifications
GENAI_TOOLS_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_executive_metrics",
            "description": "Get high-level company KPIs: total revenue, gross profit, overall profit margin percentage, total orders, active customer count, and AOV.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sales_trend",
            "description": "Get monthly historical sales, revenue, profit, and month-over-month growth trends.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Optional start date filter (YYYY-MM)"},
                    "end_date": {"type": "string", "description": "Optional end date filter (YYYY-MM)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_category_profit",
            "description": "Get category-level analytics: revenue, profit, gross margin %, and average discount rates.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_region_performance",
            "description": "Get regional performance metrics: revenue, profit margin %, order counts, and revenue share.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_segments",
            "description": "Get customer RFM segmentation clusters (Champions, Loyal, At-Risk, Occasional) with cluster statistics.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_products",
            "description": "Get the top selling or highest profit products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of products to return (default 10)"},
                    "sort_by": {"type": "string", "enum": ["revenue", "profit", "units"], "description": "Ranking metric"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_underperforming_products",
            "description": "Get underperforming products with low or negative profit margins.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of products to return"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_churn_summary",
            "description": "Get customer churn prediction metrics, population risk band distributions, and top at-risk VIPs.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "Get demand forecasting predictions, 6-month projected revenue, confidence intervals, and category trajectories.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_prescriptive_recommendations",
            "description": "Get data-grounded prescriptive business recommendations prioritized for executive action.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

TOOL_REGISTRY = {
    "get_executive_metrics": tool_get_executive_metrics,
    "get_sales_trend": tool_get_sales_trend,
    "get_category_profit": tool_get_category_profit,
    "get_region_performance": tool_get_region_performance,
    "get_customer_segments": tool_get_customer_segments,
    "get_top_products": tool_get_top_products,
    "get_underperforming_products": tool_get_underperforming_products,
    "get_churn_summary": tool_get_churn_summary,
    "get_forecast": tool_get_forecast,
    "get_prescriptive_recommendations": tool_get_prescriptive_recommendations
}
