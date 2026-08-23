"""
RetailPulse AI — Customer Churn Prediction & Risk Scoring Engine
Trains and compares Logistic Regression, Random Forest, and Gradient Boosting models.
Computes ROC-AUC, Recall, Precision, F1-Score, confusion matrix, feature importances, and risk bands.
"""

import os
import json
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib

from backend.app.analytics.data_loader import DataLoader
from backend.app.core.config import settings

MODEL_DIR = os.path.abspath(settings.MODEL_DIR)
os.makedirs(MODEL_DIR, exist_ok=True)

class ChurnPredictionEngine:
    _cached_results = None

    @classmethod
    def train_and_evaluate(cls, force_retrain: bool = False) -> Dict[str, Any]:
        """Trains multiple churn classification models, logs metrics, and selects the champion."""
        meta_path = os.path.join(MODEL_DIR, "churn_meta.json")
        model_path = os.path.join(MODEL_DIR, "churn_champion.joblib")

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
        df = DataLoader.load_customer_rfm_base()
        # Churn analysis cohort: customers with at least 1 order and >= 60 days tenure
        df_cohort = df[(df["frequency"] > 0) & (df["tenure_days"] >= 60)].copy()

        # Business Definition: Churned if recency > 180 days
        df_cohort["is_churned"] = (df_cohort["recency_days"] > 180).astype(int)

        # Feature Engineering
        df_cohort["purchase_cadence_days"] = (df_cohort["tenure_days"] / df_cohort["frequency"].clip(lower=1)).round(1)
        df_cohort["profit_per_order"] = (df_cohort["total_profit"] / df_cohort["frequency"].clip(lower=1)).round(2)

        feature_cols = [
            "frequency",
            "monetary",
            "average_order_value",
            "avg_discount_rate",
            "category_diversity",
            "tenure_days",
            "purchase_cadence_days",
            "profit_per_order"
        ]

        X = df_cohort[feature_cols].fillna(0)
        y = df_cohort["is_churned"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Define candidate models
        models = {
            "Logistic Regression": (LogisticRegression(random_state=42, max_iter=1000), True),
            "Random Forest": (RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42), False),
            "Gradient Boosting": (GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42), False)
        }

        model_comparisons = []
        best_model_name = "Gradient Boosting"
        best_roc_auc = -1.0
        fitted_models = {}

        for name, (clf, use_scaled) in models.items():
            X_tr = X_train_scaled if use_scaled else X_train
            X_te = X_test_scaled if use_scaled else X_test

            clf.fit(X_tr, y_train)
            y_pred = clf.predict(X_te)
            y_prob = clf.predict_proba(X_te)[:, 1]

            acc = float(accuracy_score(y_test, y_pred))
            prec = float(precision_score(y_test, y_pred, zero_division=0))
            rec = float(recall_score(y_test, y_pred, zero_division=0))
            f1 = float(f1_score(y_test, y_pred, zero_division=0))
            roc = float(roc_auc_score(y_test, y_prob))
            cm = confusion_matrix(y_test, y_pred).tolist()

            model_comparisons.append({
                "model_name": name,
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "roc_auc": round(roc, 4),
                "confusion_matrix": {
                    "true_negatives": int(cm[0][0]),
                    "false_positives": int(cm[0][1]),
                    "false_negatives": int(cm[1][0]),
                    "true_positives": int(cm[1][1])
                }
            })

            fitted_models[name] = clf
            if roc > best_roc_auc:
                best_roc_auc = roc
                best_model_name = name

        # Extract Feature Importances from Champion Model
        champion = fitted_models[best_model_name]
        if hasattr(champion, "feature_importances_"):
            importances = champion.feature_importances_
        else:
            importances = np.abs(champion.coef_[0])
        importances = (importances / importances.sum()).round(4)
        
        feature_importance_list = [
            {"feature": feat, "importance": float(imp)}
            for feat, imp in sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True)
        ]

        # Score All Customers to get population risk distribution
        all_probs = champion.predict_proba(X if best_model_name != "Logistic Regression" else scaler.transform(X))[:, 1]
        df_cohort["churn_probability"] = all_probs.round(4)
        df_cohort["risk_band"] = pd.cut(
            df_cohort["churn_probability"],
            bins=[-0.01, 0.30, 0.70, 1.00],
            labels=["Low Risk (<30%)", "Medium Risk (30-70%)", "High Risk (>70%)"]
        )

        risk_dist = df_cohort["risk_band"].value_counts().to_dict()
        risk_summary = [
            {"risk_band": str(k), "customer_count": int(v), "share_pct": round(v / len(df_cohort) * 100, 2)}
            for k, v in risk_dist.items()
        ]

        # Top At-Risk High-Value Customers
        high_risk_vip = df_cohort[df_cohort["risk_band"] == "High Risk (>70%)"].sort_values(by="monetary", ascending=False).head(15)
        high_risk_customers = []
        for _, row in high_risk_vip.iterrows():
            high_risk_customers.append({
                "customer_id": str(row["customer_id"]),
                "customer_name": str(row["customer_name"]),
                "region": str(row["region"]),
                "segment": str(row["segment"]),
                "total_spend": round(float(row["monetary"]), 2),
                "total_orders": int(row["frequency"]),
                "recency_days": int(row["recency_days"]),
                "churn_probability": float(row["churn_probability"]),
                "risk_band": "High Risk"
            })

        # Save Champion Artifact
        joblib.dump({"model": champion, "scaler": scaler, "features": feature_cols, "model_name": best_model_name}, model_path)

        result = {
            "champion_model": best_model_name,
            "champion_roc_auc": round(best_roc_auc, 4),
            "business_definition": "Customers with no purchase activity in the past 180 days with >= 60 days customer tenure.",
            "total_analyzed_customers": int(len(df_cohort)),
            "actual_churn_rate_pct": round(float(df_cohort["is_churned"].mean() * 100), 2),
            "model_comparisons": model_comparisons,
            "feature_importances": feature_importance_list,
            "risk_band_distribution": risk_summary,
            "top_at_risk_vip_customers": high_risk_customers
        }

        with open(meta_path, "w") as f:
            json.dump(result, f, indent=2)

        cls._cached_results = result
        return cls._cached_results
