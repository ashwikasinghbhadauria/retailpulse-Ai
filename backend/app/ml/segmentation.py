"""
RetailPulse AI — Customer Segmentation Engine (RFM + K-Means)
Computes Recency, Frequency, Monetary metrics, determines optimal k using Silhouette Score,
and automatically interprets cluster centroids into actionable business labels.
"""

import os
import json
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

from backend.app.analytics.data_loader import DataLoader
from backend.app.core.config import settings

MODEL_DIR = os.path.abspath(settings.MODEL_DIR)
os.makedirs(MODEL_DIR, exist_ok=True)

class CustomerSegmentationEngine:
    _cached_results = None

    @classmethod
    def train_and_segment(cls, force_retrain: bool = False) -> Dict[str, Any]:
        """Runs RFM computation, optimal K-Means clustering, and segment labeling."""
        meta_path = os.path.join(MODEL_DIR, "segmentation_meta.json")
        model_path = os.path.join(MODEL_DIR, "kmeans_rfm.joblib")

        if not force_retrain and cls._cached_results is not None:
            return cls._cached_results

        if not force_retrain and os.path.exists(meta_path) and os.path.exists(model_path):
            try:
                with open(meta_path, "r") as f:
                    cls._cached_results = json.load(f)
                return cls._cached_results
            except Exception:
                pass

        # Load RFM base dataset
        df_rfm = DataLoader.load_customer_rfm_base()
        # Filter customers who have made at least one order
        df_active = df_rfm[df_rfm["frequency"] > 0].copy()

        # Log transform skewed features for stability
        df_active["log_recency"] = np.log1p(df_active["recency_days"].clip(lower=0))
        df_active["log_frequency"] = np.log1p(df_active["frequency"])
        df_active["log_monetary"] = np.log1p(df_active["monetary"].clip(lower=0))

        feature_cols = ["log_recency", "log_frequency", "log_monetary"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_active[feature_cols])

        # Evaluate silhouette scores for k in [3, 4, 5]
        best_k = 4
        best_score = -1
        score_dict = {}
        
        for k in [3, 4, 5]:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            score = float(silhouette_score(X_scaled, labels, sample_size=min(5000, len(X_scaled))))
            score_dict[k] = round(score, 4)
            if score > best_score:
                best_score = score
                best_k = k

        # Fit final model with best_k
        final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        df_active["cluster"] = final_kmeans.fit_predict(X_scaled)

        # Save artifacts
        joblib.dump({"model": final_kmeans, "scaler": scaler}, model_path)

        # Analyze Cluster Characteristics to dynamically assign business labels
        cluster_summary = df_active.groupby("cluster").agg(
            recency_mean=("recency_days", "mean"),
            frequency_mean=("frequency", "mean"),
            monetary_mean=("monetary", "mean"),
            customer_count=("customer_id", "count"),
            total_revenue=("monetary", "sum"),
            total_profit=("total_profit", "sum"),
            avg_aov=("average_order_value", "mean")
        ).reset_index()

        # Dynamic label assignment based on centroid percentiles
        labels_map = {}
        for _, row in cluster_summary.iterrows():
            cid = int(row["cluster"])
            r = row["recency_mean"]
            f = row["frequency_mean"]
            m = row["monetary_mean"]

            if m >= cluster_summary["monetary_mean"].quantile(0.70) and f >= cluster_summary["frequency_mean"].quantile(0.60):
                labels_map[cid] = "Champions / High Value"
            elif r > cluster_summary["recency_mean"].quantile(0.65) and f >= cluster_summary["frequency_mean"].quantile(0.40):
                labels_map[cid] = "At Risk / Inactive"
            elif f >= cluster_summary["frequency_mean"].quantile(0.40) and r <= cluster_summary["recency_mean"].quantile(0.50):
                labels_map[cid] = "Loyal Regulars"
            elif r <= cluster_summary["recency_mean"].quantile(0.40) and f < cluster_summary["frequency_mean"].quantile(0.50):
                labels_map[cid] = "Potential Growth / Recent"
            else:
                labels_map[cid] = "Occasional Buyers"

        # Fallback deduplication of names if any conflict
        assigned = set()
        for cid in labels_map:
            name = labels_map[cid]
            if name in assigned:
                labels_map[cid] = f"{name} (Tier {cid+1})"
            assigned.add(labels_map[cid])

        cluster_summary["segment_name"] = cluster_summary["cluster"].map(labels_map)
        cluster_summary["revenue_share_pct"] = (cluster_summary["total_revenue"] / cluster_summary["total_revenue"].sum() * 100).round(2)
        cluster_summary["customer_share_pct"] = (cluster_summary["customer_count"] / len(df_active) * 100).round(2)

        # Build clean output JSON
        segments_output = []
        for _, row in cluster_summary.sort_values(by="total_revenue", ascending=False).iterrows():
            segments_output.append({
                "cluster_id": int(row["cluster"]),
                "segment_name": str(row["segment_name"]),
                "customer_count": int(row["customer_count"]),
                "customer_share_pct": float(row["customer_share_pct"]),
                "total_revenue": round(float(row["total_revenue"]), 2),
                "total_profit": round(float(row["total_profit"]), 2),
                "revenue_share_pct": float(row["revenue_share_pct"]),
                "avg_recency_days": round(float(row["recency_mean"]), 1),
                "avg_frequency": round(float(row["frequency_mean"]), 1),
                "avg_monetary": round(float(row["monetary_mean"]), 2),
                "avg_order_value": round(float(row["avg_aov"]), 2)
            })

        result = {
            "optimal_k": best_k,
            "best_silhouette_score": round(best_score, 4),
            "all_evaluated_scores": score_dict,
            "total_segmented_customers": int(len(df_active)),
            "segments": segments_output
        }

        with open(meta_path, "w") as f:
            json.dump(result, f, indent=2)

        cls._cached_results = result
        return cls._cached_results
