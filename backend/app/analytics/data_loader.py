"""
RetailPulse AI — Analytics Data Loader & Preprocessing Pipeline
Provides robust data ingestion, caching, validation, and type harmonization.
"""

import os
import pandas as pd
from sqlalchemy import text
from backend.app.core.database import engine

class DataLoader:
    _cached_master = None
    _cached_rfm = None
    _cached_monthly = None

    @classmethod
    def load_master_data(cls, force_reload: bool = False) -> pd.DataFrame:
        """Loads complete denormalized transaction data with validation."""
        if cls._cached_master is not None and not force_reload:
            return cls._cached_master

        query = "SELECT * FROM v_analytics_order_items"
        try:
            with engine.connect() as conn:
                df = pd.read_sql(text(query), con=conn)
        except Exception:
            # Fallback to direct raw CSV if DB connection unavailable
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "data", "raw", "retail_transactions_master.csv")
            df = pd.read_csv(csv_path)

        # Validation & Type Conversion
        df["order_date"] = pd.to_datetime(df["order_date"])
        df["signup_date"] = pd.to_datetime(df["signup_date"])
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
        df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
        df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(0.0)
        
        # Deduplication check
        df = df.drop_duplicates(subset=["order_item_id"])

        cls._cached_master = df
        return cls._cached_master

    @classmethod
    def load_customer_rfm_base(cls, force_reload: bool = False) -> pd.DataFrame:
        """Loads customer-level aggregated RFM metrics."""
        if cls._cached_rfm is not None and not force_reload:
            return cls._cached_rfm

        query = "SELECT * FROM v_customer_rfm_base"
        with engine.connect() as conn:
            df = pd.read_sql(text(query), con=conn)

        df["signup_date"] = pd.to_datetime(df["signup_date"])
        df["first_order_date"] = pd.to_datetime(df["first_order_date"])
        df["last_order_date"] = pd.to_datetime(df["last_order_date"])
        df["recency_days"] = pd.to_numeric(df["recency_days"], errors="coerce").fillna(999).astype(int)
        df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce").fillna(0).astype(int)
        df["monetary"] = pd.to_numeric(df["monetary"], errors="coerce").fillna(0.0)
        df["total_profit"] = pd.to_numeric(df["total_profit"], errors="coerce").fillna(0.0)
        df["average_order_value"] = pd.to_numeric(df["average_order_value"], errors="coerce").fillna(0.0)

        cls._cached_rfm = df
        return cls._cached_rfm

    @classmethod
    def load_monthly_trends(cls, force_reload: bool = False) -> pd.DataFrame:
        """Loads monthly sales summary metrics."""
        if cls._cached_monthly is not None and not force_reload:
            return cls._cached_monthly

        query = "SELECT * FROM v_monthly_sales_summary ORDER BY year_month ASC"
        with engine.connect() as conn:
            df = pd.read_sql(text(query), con=conn)

        cls._cached_monthly = df
        return cls._cached_monthly
