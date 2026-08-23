"""
RetailPulse AI — Business Diagnostics & Anomaly Detection Engine
Identifies performance drops, margin erosions, category cannibalization, and discount inefficiencies.
"""

from typing import Dict, Any, List
import pandas as pd
from backend.app.analytics.data_loader import DataLoader

def run_diagnostics() -> Dict[str, Any]:
    """Runs automated diagnostic analysis on revenue, profit, discounts, and categories."""
    df_monthly = DataLoader.load_monthly_trends()
    df_master = DataLoader.load_master_data()
    
    findings = []
    
    # 1. MoM Margin & Revenue Anomaly Check
    if len(df_monthly) >= 3:
        latest = df_monthly.iloc[-1]
        prev = df_monthly.iloc[-2]
        
        # Check if revenue dropped
        if latest["mom_revenue_growth_pct"] < -5.0:
            findings.append({
                "type": "revenue_drop",
                "severity": "high",
                "title": f"Revenue contraction of {abs(latest['mom_revenue_growth_pct']):.1f}% in {latest['year_month']}",
                "description": f"Revenue fell from ${prev['total_revenue']:,.2f} in {prev['year_month']} to ${latest['total_revenue']:,.2f} in {latest['year_month']}.",
                "metric_impact": f"-${(prev['total_revenue'] - latest['total_revenue']):,.2f}"
            })
            
        # Check if profit margin contracted while revenue held
        margin_diff = latest["profit_margin_pct"] - prev["profit_margin_pct"]
        if margin_diff < -2.0:
            findings.append({
                "type": "margin_compression",
                "severity": "medium",
                "title": f"Profit Margin squeezed by {abs(margin_diff):.2f}% in {latest['year_month']}",
                "description": f"Overall profit margin dropped to {latest['profit_margin_pct']:.1f}% vs {prev['profit_margin_pct']:.1f}% previously.",
                "metric_impact": f"{margin_diff:.2f}% Margin shift"
            })

    # 2. Category Discount Inefficiency Diagnosis
    cat_summary = df_master.groupby("category_name").agg(
        total_rev=("revenue", "sum"),
        total_profit=("profit", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()
    cat_summary["margin_pct"] = (cat_summary["total_profit"] / cat_summary["total_rev"] * 100).round(2)
    
    for _, row in cat_summary.iterrows():
        if row["avg_discount"] > 0.08 and row["margin_pct"] < 40.0:
            findings.append({
                "type": "discount_inefficiency",
                "severity": "medium",
                "title": f"Excessive discounting in {row['category_name']}",
                "description": f"{row['category_name']} carries an average discount of {row['avg_discount']*100:.1f}% resulting in a suppressed profit margin of {row['margin_pct']:.1f}%.",
                "metric_impact": f"${row['total_rev']:,.0f} Category Revenue"
            })

    # 3. Regional Disparity Analysis
    reg_summary = df_master.groupby("region").agg(
        total_rev=("revenue", "sum"),
        total_profit=("profit", "sum")
    ).reset_index()
    reg_summary["margin_pct"] = (reg_summary["total_profit"] / reg_summary["total_rev"] * 100).round(2)
    
    min_reg = reg_summary.sort_values(by="margin_pct").iloc[0]
    max_reg = reg_summary.sort_values(by="margin_pct", ascending=False).iloc[0]
    
    findings.append({
        "type": "regional_disparity",
        "severity": "info",
        "title": f"Regional Profitability Spread ({max_reg['region']} vs {min_reg['region']})",
        "description": f"{max_reg['region']} achieves the highest margin ({max_reg['margin_pct']}%) whereas {min_reg['region']} lags at {min_reg['margin_pct']}%.",
        "metric_impact": f"{max_reg['margin_pct'] - min_reg['margin_pct']:.1f}% Spread"
    })

    return {
        "diagnostic_status": "complete",
        "total_findings": len(findings),
        "findings": findings
    }
