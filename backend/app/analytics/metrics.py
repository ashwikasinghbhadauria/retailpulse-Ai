"""
RetailPulse AI — Descriptive & Diagnostic Metrics Calculation Engine
Provides structured business KPIs, regional breakdowns, category profitability, and product rankings.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from backend.app.analytics.data_loader import DataLoader

def get_executive_summary() -> Dict[str, Any]:
    """Calculates top-level executive KPIs and overarching business metrics."""
    df_monthly = DataLoader.load_monthly_trends()
    df_rfm = DataLoader.load_customer_rfm_base()

    total_revenue = float(df_monthly["total_revenue"].sum())
    total_profit = float(df_monthly["total_profit"].sum())
    overall_margin_pct = round((total_profit / total_revenue) * 100, 2) if total_revenue > 0 else 0.0
    total_orders = int(df_monthly["total_orders"].sum())
    total_customers = int(len(df_rfm))
    active_customers = int((df_rfm["frequency"] > 0).sum())
    aov = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0

    # Latest month vs previous month
    if len(df_monthly) >= 2:
        latest = df_monthly.iloc[-1]
        prev = df_monthly.iloc[-2]
        latest_month = str(latest["year_month"])
        latest_revenue = float(latest["total_revenue"])
        latest_profit = float(latest["total_profit"])
        mom_revenue_growth = float(latest["mom_revenue_growth_pct"]) if pd.notna(latest["mom_revenue_growth_pct"]) else 0.0
        mom_profit_growth = float(latest["mom_profit_growth_pct"]) if pd.notna(latest["mom_profit_growth_pct"]) else 0.0
    else:
        latest_month = "Current"
        latest_revenue = total_revenue
        latest_profit = total_profit
        mom_revenue_growth = 0.0
        mom_profit_growth = 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "overall_margin_pct": overall_margin_pct,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "active_customers": active_customers,
        "average_order_value": aov,
        "latest_month": latest_month,
        "latest_monthly_revenue": round(latest_revenue, 2),
        "latest_monthly_profit": round(latest_profit, 2),
        "mom_revenue_growth_pct": mom_revenue_growth,
        "mom_profit_growth_pct": mom_profit_growth
    }

def get_sales_trends(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns monthly sales, profit, orders, and growth trends."""
    df = DataLoader.load_monthly_trends()
    if start_date:
        df = df[df["year_month"] >= start_date[:7]]
    if end_date:
        df = df[df["year_month"] <= end_date[:7]]

    records = []
    for _, row in df.iterrows():
        records.append({
            "year_month": str(row["year_month"]),
            "total_orders": int(row["total_orders"]),
            "active_customers": int(row["active_customers"]),
            "total_units_sold": int(row["total_units_sold"]),
            "total_revenue": round(float(row["total_revenue"]), 2),
            "total_profit": round(float(row["total_profit"]), 2),
            "profit_margin_pct": round(float(row["profit_margin_pct"]), 2),
            "avg_discount_pct": round(float(row["avg_discount_pct"]), 2),
            "average_order_value": round(float(row["average_order_value"]), 2),
            "mom_revenue_growth_pct": round(float(row["mom_revenue_growth_pct"]), 2) if pd.notna(row["mom_revenue_growth_pct"]) else 0.0,
            "mom_profit_growth_pct": round(float(row["mom_profit_growth_pct"]), 2) if pd.notna(row["mom_profit_growth_pct"]) else 0.0
        })
    return records

def get_regional_breakdown() -> List[Dict[str, Any]]:
    """Returns regional sales volume, revenue, profit, margin %, and AOV."""
    df_master = DataLoader.load_master_data()
    reg = df_master.groupby("region").agg(
        total_orders=("order_id", "nunique"),
        total_customers=("customer_id", "nunique"),
        total_units_sold=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()

    total_all_rev = reg["total_revenue"].sum()
    records = []
    for _, row in reg.sort_values(by="total_revenue", ascending=False).iterrows():
        rev = float(row["total_revenue"])
        prof = float(row["total_profit"])
        margin = round((prof / rev) * 100, 2) if rev > 0 else 0.0
        records.append({
            "region": str(row["region"]),
            "total_orders": int(row["total_orders"]),
            "total_customers": int(row["total_customers"]),
            "total_units_sold": int(row["total_units_sold"]),
            "total_revenue": round(rev, 2),
            "total_profit": round(prof, 2),
            "profit_margin_pct": margin,
            "revenue_share_pct": round((rev / total_all_rev) * 100, 2) if total_all_rev > 0 else 0.0,
            "average_order_value": round(rev / row["total_orders"], 2) if row["total_orders"] > 0 else 0.0,
            "avg_discount_pct": round(float(row["avg_discount"]) * 100, 2)
        })
    return records

def get_category_breakdown() -> List[Dict[str, Any]]:
    """Returns category sales, profits, unit volumes, and profit margins."""
    df_master = DataLoader.load_master_data()
    cat = df_master.groupby(["category_id", "category_name"]).agg(
        product_count=("product_id", "nunique"),
        total_orders=("order_id", "nunique"),
        total_units_sold=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()

    total_all_rev = cat["total_revenue"].sum()
    records = []
    for _, row in cat.sort_values(by="total_revenue", ascending=False).iterrows():
        rev = float(row["total_revenue"])
        prof = float(row["total_profit"])
        margin = round((prof / rev) * 100, 2) if rev > 0 else 0.0
        records.append({
            "category_id": str(row["category_id"]),
            "category_name": str(row["category_name"]),
            "product_count": int(row["product_count"]),
            "total_orders": int(row["total_orders"]),
            "total_units_sold": int(row["total_units_sold"]),
            "total_revenue": round(rev, 2),
            "total_profit": round(prof, 2),
            "profit_margin_pct": margin,
            "revenue_share_pct": round((rev / total_all_rev) * 100, 2) if total_all_rev > 0 else 0.0,
            "avg_discount_pct": round(float(row["avg_discount"]) * 100, 2)
        })
    return records

def get_top_products(limit: int = 10, sort_by: str = "revenue") -> List[Dict[str, Any]]:
    """Returns top products sorted by revenue, profit, or units sold."""
    df_master = DataLoader.load_master_data()
    prod = df_master.groupby(["product_id", "product_name", "category_name"]).agg(
        price=("unit_price", "mean"),
        total_orders=("order_id", "nunique"),
        total_units_sold=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()

    prod["gross_margin_pct"] = (prod["total_profit"] / prod["total_revenue"] * 100).round(2)
    sort_col = "total_revenue" if sort_by == "revenue" else ("total_profit" if sort_by == "profit" else "total_units_sold")
    prod = prod.sort_values(by=sort_col, ascending=False).head(limit)

    records = []
    for _, row in prod.iterrows():
        records.append({
            "product_id": str(row["product_id"]),
            "product_name": str(row["product_name"]),
            "category_name": str(row["category_name"]),
            "price": round(float(row["price"]), 2),
            "total_orders": int(row["total_orders"]),
            "total_units_sold": int(row["total_units_sold"]),
            "total_revenue": round(float(row["total_revenue"]), 2),
            "total_profit": round(float(row["total_profit"]), 2),
            "gross_margin_pct": float(row["gross_margin_pct"]),
            "avg_discount_pct": round(float(row["avg_discount"]) * 100, 2)
        })
    return records

def get_underperforming_products(limit: int = 10) -> List[Dict[str, Any]]:
    """Returns products with lowest profit margins or margin erosion."""
    df_master = DataLoader.load_master_data()
    prod = df_master.groupby(["product_id", "product_name", "category_name"]).agg(
        price=("unit_price", "mean"),
        total_orders=("order_id", "nunique"),
        total_units_sold=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()

    prod["gross_margin_pct"] = (prod["total_profit"] / prod["total_revenue"] * 100).round(2)
    prod = prod[prod["total_revenue"] > 1000].sort_values(by="gross_margin_pct", ascending=True).head(limit)

    records = []
    for _, row in prod.iterrows():
        records.append({
            "product_id": str(row["product_id"]),
            "product_name": str(row["product_name"]),
            "category_name": str(row["category_name"]),
            "price": round(float(row["price"]), 2),
            "total_orders": int(row["total_orders"]),
            "total_units_sold": int(row["total_units_sold"]),
            "total_revenue": round(float(row["total_revenue"]), 2),
            "total_profit": round(float(row["total_profit"]), 2),
            "gross_margin_pct": float(row["gross_margin_pct"]),
            "avg_discount_pct": round(float(row["avg_discount"]) * 100, 2),
            "risk_flag": "Low Margin / High Discount" if row["avg_discount"] > 0.15 else "Underperforming Margin"
        })
    return records
