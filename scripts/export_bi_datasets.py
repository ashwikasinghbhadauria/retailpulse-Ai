"""
RetailPulse AI — Power BI & Tableau Analytics Dataset Exporter
Transforms database tables into optimized star-schema tables and flat extracts for BI tools.
"""

import os
import sys
import pandas as pd
import numpy as np

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.analytics.data_loader import DataLoader
from backend.app.ml.segmentation import CustomerSegmentationEngine
from backend.app.ml.churn import ChurnPredictionEngine
from backend.app.ml.forecasting import DemandForecastingEngine

PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def export_bi_datasets():
    print("Exporting optimized Power BI and Tableau datasets...")
    
    # 1. Master Transactions
    df_master = DataLoader.load_master_data(force_reload=True).copy()
    
    # 2. Add RFM & Churn Annotations to Customer Dimension
    seg_data = CustomerSegmentationEngine.train_and_segment()
    churn_data = ChurnPredictionEngine.train_and_evaluate()
    df_rfm = DataLoader.load_customer_rfm_base()

    # Create customer intelligence table
    df_dim_customers = df_rfm.copy()
    
    # Map churn probabilities and risk bands
    vip_churn_map = {c["customer_id"]: c["churn_probability"] for c in churn_data.get("top_at_risk_vip_customers", [])}
    df_dim_customers["churn_probability"] = df_dim_customers["customer_id"].map(vip_churn_map).fillna(0.35)
    df_dim_customers["churn_risk_band"] = np.where(
        df_dim_customers["recency_days"] > 180, "High Risk (>70%)",
        np.where(df_dim_customers["recency_days"] > 90, "Medium Risk (30-70%)", "Low Risk (<30%)")
    )
    
    # 3. Calendar Dimension
    min_date = df_master["order_date"].min()
    max_date = pd.to_datetime("2026-12-31")
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    df_dim_date = pd.DataFrame({
        "Date": date_range,
        "Year": date_range.year,
        "Quarter": "Q" + date_range.quarter.astype(str),
        "Month": date_range.month,
        "MonthName": date_range.strftime("%B"),
        "YearMonth": date_range.strftime("%Y-%m"),
        "DayOfWeek": date_range.day_name(),
        "DayNumber": date_range.dayofweek + 1,
        "IsWeekend": date_range.dayofweek.isin([5, 6]).astype(int)
    })

    # 4. Export Power BI Star Schema Tables
    df_master.to_csv(os.path.join(PROCESSED_DIR, "powerbi_fact_sales.csv"), index=False)
    df_dim_customers.to_csv(os.path.join(PROCESSED_DIR, "powerbi_dim_customers.csv"), index=False)
    df_dim_date.to_csv(os.path.join(PROCESSED_DIR, "powerbi_dim_date.csv"), index=False)

    # 5. Export Tableau Flat Analytics Extract
    df_master["churn_risk_band"] = df_master["customer_id"].map(
        df_dim_customers.set_index("customer_id")["churn_risk_band"].to_dict()
    ).fillna("Low Risk (<30%)")
    df_master.to_csv(os.path.join(PROCESSED_DIR, "tableau_retail_master_extract.csv"), index=False)

    print(f"Power BI & Tableau datasets successfully exported to {PROCESSED_DIR}")

if __name__ == "__main__":
    export_bi_datasets()
