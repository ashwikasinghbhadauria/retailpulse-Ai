"""
RetailPulse AI — ML Pipeline Training and Evaluation Script
Executes RFM Customer Segmentation, Customer Churn Modeling, and Demand Forecasting.
"""

import os
import sys
import time

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.analytics.metrics import get_executive_summary
from backend.app.ml.segmentation import CustomerSegmentationEngine
from backend.app.ml.churn import ChurnPredictionEngine
from backend.app.ml.forecasting import DemandForecastingEngine

def main():
    print("=" * 60)
    print("  RETAILPULSE AI — ML & ANALYTICS PIPELINE RUNNER")
    print("=" * 60)
    start_all = time.time()

    # 1. Executive Summary
    print("\n[1/4] Calculating Executive KPIs...")
    kpis = get_executive_summary()
    print(f"  - Total Revenue:    ${kpis['total_revenue']:,.2f}")
    print(f"  - Total Profit:     ${kpis['total_profit']:,.2f}")
    print(f"  - Profit Margin:    {kpis['overall_margin_pct']}%")
    print(f"  - Total Orders:     {kpis['total_orders']:,}")
    print(f"  - Total Customers:  {kpis['total_customers']:,}")
    print(f"  - AOV:              ${kpis['average_order_value']:.2f}")

    # 2. RFM Segmentation
    print("\n[2/4] Executing RFM Customer Segmentation (K-Means)...")
    t0 = time.time()
    seg = CustomerSegmentationEngine.train_and_segment(force_retrain=True)
    print(f"  - Optimal k:            {seg['optimal_k']}")
    print(f"  - Silhouette Score:     {seg['best_silhouette_score']:.4f}")
    print(f"  - Segmented Customers:  {seg['total_segmented_customers']:,}")
    for s in seg['segments']:
        print(f"    * {s['segment_name']:<28}: {s['customer_count']:>5,} customers ({s['customer_share_pct']:>5.1f}%) | ${s['total_revenue']:>12,.2f} rev | Recency: {s['avg_recency_days']:.0f}d")
    print(f"  Completed in {time.time() - t0:.2f}s")

    # 3. Customer Churn Prediction
    print("\n[3/4] Training & Comparing Customer Churn Models...")
    t0 = time.time()
    churn = ChurnPredictionEngine.train_and_evaluate(force_retrain=True)
    print(f"  - Champion Model: {churn['champion_model']}")
    print(f"  - Champion ROC-AUC: {churn['champion_roc_auc']:.4f}")
    print(f"  - Baseline Churn Rate: {churn['actual_churn_rate_pct']}%")
    print("  - Model Leaderboard:")
    for m in churn['model_comparisons']:
        print(f"    * {m['model_name']:<20}: ROC-AUC={m['roc_auc']:.4f} | Recall={m['recall']:.4f} | Prec={m['precision']:.4f} | F1={m['f1_score']:.4f}")
    print("  - Risk Band Distribution:")
    for r in churn['risk_band_distribution']:
        print(f"    * {r['risk_band']:<22}: {r['customer_count']:>5,} customers ({r['share_pct']:>5.1f}%)")
    print(f"  Completed in {time.time() - t0:.2f}s")

    # 4. Demand Forecasting
    print("\n[4/4] Generating Demand Forecast & Horizon Modeling...")
    t0 = time.time()
    fc = DemandForecastingEngine.generate_forecast(force_retrain=True)
    print(f"  - Forecaster:           {fc['model_architecture']}")
    print(f"  - Validation MAPE:      {fc['validation_metrics']['champion_mape']}%")
    print(f"  - Horizon:              {fc['forecast_horizon_months']} Months")
    print(f"  - Q4 Projected Revenue: ${fc['next_quarter_projected_revenue']:,.2f}")
    print(f"  Completed in {time.time() - t0:.2f}s")

    print(f"\nAll ML pipelines and analytical models successfully trained and verified in {time.time() - start_all:.2f}s.")

if __name__ == "__main__":
    main()
