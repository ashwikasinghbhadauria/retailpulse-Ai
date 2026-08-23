# RetailPulse AI — Machine Learning Model Cards

This document provides model governance, architecture, performance, feature importance, and operational guidelines for the predictive models deployed in RetailPulse AI.

---

## 1. Customer Churn Classification Model

### Model Details
- **Developer**: RetailPulse AI Engineering Team
- **Model Type**: Supervised Binary Classification (Ensemble & Linear Models)
- **Champion Architecture**: Random Forest Classifier (`sklearn.ensemble.RandomForestClassifier`) / Gradient Boosting
- **Target Variable**: `is_churned` (1 = Churned, 0 = Active)
- **Business Definition**: Customer with >= 60 days tenure and zero purchase activity in the past 180 days.

### Features
1. `frequency`: Total historical orders count.
2. `monetary`: Total cumulative gross revenue.
3. `average_order_value`: Average spend per completed order.
4. `avg_discount_rate`: Historical mean markdown percentage.
5. `category_diversity`: Count of distinct categories bought.
6. `tenure_days`: Account age in days since signup.
7. `purchase_cadence_days`: Mean elapsed days between purchases.
8. `profit_per_order`: Average gross profit generated per order.

### Performance Benchmark (25% Stratified Holdout Test)
| Model Architecture | ROC-AUC | Recall | Precision | F1-Score | Accuracy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest (Champion)** | **0.7842** | **0.8462** | **0.7111** | **0.7728** | **74.8%** |
| Gradient Boosting | 0.7838 | 0.8407 | 0.7157 | 0.7732 | 75.0% |
| Logistic Regression | 0.7805 | 0.7961 | 0.7095 | 0.7503 | 73.1% |

### Risk Bands Calibration
- **Low Risk (<30%)**: Stable active regular customers.
- **Medium Risk (30–70%)**: Elongated purchase intervals, potential cooling off.
- **High Risk (>70%)**: Critical attrition likelihood requiring immediate win-back campaigns.

---

## 2. Customer RFM Segmentation Model

### Model Details
- **Architecture**: Unsupervised K-Means Clustering (`sklearn.cluster.KMeans`)
- **Optimization Criterion**: Silhouette Score across \(k \in [3, 4, 5]\)
- **Optimal Cluster Count**: \(k = 4\) (Silhouette Score: **0.3302**)
- **Preprocessing**: Natural log scaling (`np.log1p`) + `StandardScaler` to normalize skewed financial distributions.

### Segment Persona Definitions
1. **Champions / High Value**: High monetary spend ($3,000+), high frequency (8+ orders), low recency (<60 days). Generates >48% of total gross revenue.
2. **Loyal Regulars**: Steady frequency (4–7 orders), moderate monetary, recency < 90 days.
3. **Potential Growth / Recent**: Recent signups with 1–2 orders and high average basket size.
4. **At Risk / Inactive**: Historical buyers with long inactivity (>180 days).

---

## 3. Demand Forecasting Model

### Model Details
- **Architecture**: Multi-step Autoregressive Gradient Boosting Regressor
- **Features**: Lag variables (\(y_{t-1}, y_{t-2}, y_{t-3}\)), Rolling 3-month mean, Linear trend index, Trigonometric cyclical month encodings (\(\sin(2\pi m/12), \cos(2\pi m/12)\)).
- **Horizon**: 6 Months forward.
- **Uncertainty**: 90% Confidence Interval generated via empirical error residual standard deviation.
- **Holdout Validation**: MAPE: **25.99%** vs naive rolling baseline (28.4%).
