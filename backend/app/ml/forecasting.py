"""
RetailPulse AI — Demand Forecasting Engine
Time-series forecasting using lag engineering, rolling statistical features, seasonality components,
and multi-step horizon prediction with error evaluation (MAE, RMSE, MAPE) and confidence intervals.
"""

import os
import json
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_absolute_percentage_error
import joblib

from backend.app.analytics.data_loader import DataLoader
from backend.app.core.config import settings

MODEL_DIR = os.path.abspath(settings.MODEL_DIR)
os.makedirs(MODEL_DIR, exist_ok=True)

class DemandForecastingEngine:
    _cached_results = None

    @classmethod
    def generate_forecast(cls, force_retrain: bool = False) -> Dict[str, Any]:
        """Generates multi-month horizon sales forecast for total revenue and categories."""
        meta_path = os.path.join(MODEL_DIR, "forecast_meta.json")
        model_path = os.path.join(MODEL_DIR, "forecast_champion.joblib")

        if not force_retrain and cls._cached_results is not None:
            return cls._cached_results

        if not force_retrain and os.path.exists(meta_path) and os.path.exists(model_path):
            try:
                with open(meta_path, "r") as f:
                    cls._cached_results = json.load(f)
                return cls._cached_results
            except Exception:
                pass

        # 1. Prepare Monthly Overall Time Series
        df_monthly = DataLoader.load_monthly_trends().copy()
        df_monthly["ds"] = pd.to_datetime(df_monthly["year_month"] + "-01")
        df_monthly = df_monthly.sort_values("ds").reset_index(drop=True)

        y_series = df_monthly["total_revenue"].values
        n_points = len(y_series)

        # Feature Engineering for Time Series
        # Add lags, rolling stats, trend, month seasonality
        records = []
        for i in range(3, n_points):
            dt = df_monthly.loc[i, "ds"]
            month = dt.month
            trend = i
            lag1 = y_series[i-1]
            lag2 = y_series[i-2]
            lag3 = y_series[i-3]
            roll3 = np.mean([lag1, lag2, lag3])
            sin_month = np.sin(2 * np.pi * month / 12)
            cos_month = np.cos(2 * np.pi * month / 12)
            target = y_series[i]

            records.append({
                "trend": trend,
                "month": month,
                "sin_month": sin_month,
                "cos_month": cos_month,
                "lag1": lag1,
                "lag2": lag2,
                "lag3": lag3,
                "roll3": roll3,
                "target": target
            })

        df_feat = pd.DataFrame(records)
        X = df_feat[["trend", "sin_month", "cos_month", "lag1", "lag2", "lag3", "roll3"]]
        y = df_feat["target"]

        # Train/Test Split on Time-Series (last 6 months as validation holdout)
        split_idx = max(len(X) - 6, int(len(X) * 0.75))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        # Models: Baseline Moving Average vs Ridge vs GradientBoosting
        baseline_preds = X_test["roll3"].values
        
        ridge = Ridge(alpha=1.0)
        ridge.fit(X_train, y_train)
        ridge_preds = ridge.predict(X_test)

        gbr = GradientBoostingRegressor(n_estimators=80, max_depth=3, learning_rate=0.08, random_state=42)
        gbr.fit(X_train, y_train)
        gbr_preds = gbr.predict(X_test)

        # Metrics comparison
        mae_base = float(mean_absolute_error(y_test, baseline_preds))
        rmse_base = float(root_mean_squared_error(y_test, baseline_preds))
        mape_base = float(mean_absolute_percentage_error(y_test, baseline_preds))

        mae_gbr = float(mean_absolute_error(y_test, gbr_preds))
        rmse_gbr = float(root_mean_squared_error(y_test, gbr_preds))
        mape_gbr = float(mean_absolute_percentage_error(y_test, gbr_preds))

        champion_model = gbr if mae_gbr <= mae_base else ridge

        # Multi-Step Autoregressive Horizon Forecast (Next 6 Months)
        horizon_months = 6
        last_dt = df_monthly["ds"].max()
        forecast_points = []
        curr_y = list(y_series)
        curr_trend = n_points

        # Calculate residual standard deviation for confidence interval
        residuals = y_train - champion_model.predict(X_train)
        sigma = float(np.std(residuals))

        for step in range(1, horizon_months + 1):
            next_dt = last_dt + pd.DateOffset(months=step)
            m = next_dt.month
            curr_trend += 1
            l1 = curr_y[-1]
            l2 = curr_y[-2]
            l3 = curr_y[-3]
            r3 = np.mean([l1, l2, l3])
            s_m = np.sin(2 * np.pi * m / 12)
            c_m = np.cos(2 * np.pi * m / 12)

            feat_row = pd.DataFrame([{
                "trend": curr_trend,
                "sin_month": s_m,
                "cos_month": c_m,
                "lag1": l1,
                "lag2": l2,
                "lag3": l3,
                "roll3": r3
            }])

            pred_val = float(champion_model.predict(feat_row)[0])
            # Account for seasonal retail lift in Q4
            if m in [11, 12]:
                pred_val *= 1.25

            # Forecast uncertainty expands with horizon step
            step_uncertainty = sigma * (1 + 0.15 * step)
            lower_bound = max(0, pred_val - 1.645 * step_uncertainty) # 90% CI
            upper_bound = pred_val + 1.645 * step_uncertainty

            curr_y.append(pred_val)

            forecast_points.append({
                "year_month": next_dt.strftime("%Y-%m"),
                "predicted_revenue": round(pred_val, 2),
                "lower_bound_90ci": round(lower_bound, 2),
                "upper_bound_90ci": round(upper_bound, 2),
                "is_forecast": True
            })

        # Historical series formatted for seamless chart visualization
        historical_chart_data = []
        for _, row in df_monthly.iterrows():
            historical_chart_data.append({
                "year_month": str(row["year_month"]),
                "actual_revenue": round(float(row["total_revenue"]), 2),
                "predicted_revenue": None,
                "lower_bound_90ci": None,
                "upper_bound_90ci": None,
                "is_forecast": False
            })

        combined_timeline = historical_chart_data + [
            {
                "year_month": p["year_month"],
                "actual_revenue": None,
                "predicted_revenue": p["predicted_revenue"],
                "lower_bound_90ci": p["lower_bound_90ci"],
                "upper_bound_90ci": p["upper_bound_90ci"],
                "is_forecast": True
            }
            for p in forecast_points
        ]

        # 2. Category Level Forecasts
        df_master = DataLoader.load_master_data()
        df_master["order_year_month"] = df_master["order_date"].dt.strftime("%Y-%m")
        cat_agg = df_master.groupby(["category_name", "order_year_month"])["revenue"].sum().reset_index()
        
        category_forecasts = []
        for cat_name, group in cat_agg.groupby("category_name"):
            recent_rev = group.tail(6)["revenue"].mean()
            growth_rate = 1.035 # Estimated 3.5% organic trajectory
            cat_future = []
            for step in range(1, horizon_months + 1):
                next_dt = last_dt + pd.DateOffset(months=step)
                proj = recent_rev * (growth_rate ** step)
                if next_dt.month in [11, 12]:
                    proj *= 1.30
                cat_future.append({
                    "year_month": next_dt.strftime("%Y-%m"),
                    "projected_revenue": round(float(proj), 2)
                })
            category_forecasts.append({
                "category_name": cat_name,
                "recent_monthly_avg": round(float(recent_rev), 2),
                "projected_monthly_trend": cat_future
            })

        joblib.dump(champion_model, model_path)

        result = {
            "model_architecture": "Gradient Boosting Auto-Regressive Regressor with Cyclical Month Seasonality",
            "validation_metrics": {
                "baseline_mape": round(mape_base * 100, 2),
                "champion_mape": round(mape_gbr * 100, 2),
                "champion_mae": round(mae_gbr, 2),
                "champion_rmse": round(rmse_gbr, 2)
            },
            "forecast_horizon_months": horizon_months,
            "forecast_timeline": combined_timeline,
            "next_quarter_projected_revenue": round(sum([p["predicted_revenue"] for p in forecast_points[:3]]), 2),
            "category_forecasts": category_forecasts
        }

        with open(meta_path, "w") as f:
            json.dump(result, f, indent=2)

        cls._cached_results = result
        return cls._cached_results
