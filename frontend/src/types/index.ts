export interface ExecutiveSummary {
  total_revenue: number;
  total_profit: number;
  overall_margin_pct: number;
  total_orders: number;
  total_customers: number;
  active_customers: number;
  average_order_value: number;
  latest_month: string;
  latest_monthly_revenue: number;
  latest_monthly_profit: number;
  mom_revenue_growth_pct: number;
  mom_profit_growth_pct: number;
}

export interface MonthlyTrend {
  year_month: string;
  total_orders: number;
  active_customers: number;
  total_units_sold: number;
  total_revenue: number;
  total_profit: number;
  profit_margin_pct: number;
  avg_discount_pct: number;
  average_order_value: number;
  mom_revenue_growth_pct: number;
  mom_profit_growth_pct: number;
}

export interface RegionalMetric {
  region: string;
  total_orders: number;
  total_customers: number;
  total_units_sold: number;
  total_revenue: number;
  total_profit: number;
  profit_margin_pct: number;
  revenue_share_pct: number;
  average_order_value: number;
  avg_discount_pct: number;
}

export interface CategoryMetric {
  category_id: string;
  category_name: string;
  product_count: number;
  total_orders: number;
  total_units_sold: number;
  total_revenue: number;
  total_profit: number;
  profit_margin_pct: number;
  revenue_share_pct: number;
  avg_discount_pct: number;
}

export interface ProductMetric {
  product_id: string;
  product_name: string;
  category_name: string;
  price: number;
  total_orders: number;
  total_units_sold: number;
  total_revenue: number;
  total_profit: number;
  gross_margin_pct: number;
  avg_discount_pct: number;
  risk_flag?: string;
}

export interface CustomerSegment {
  cluster_id: number;
  segment_name: string;
  customer_count: number;
  customer_share_pct: number;
  total_revenue: number;
  total_profit: number;
  revenue_share_pct: number;
  avg_recency_days: number;
  avg_frequency: number;
  avg_monetary: number;
  avg_order_value: number;
}

export interface SegmentationResponse {
  optimal_k: number;
  best_silhouette_score: number;
  all_evaluated_scores: Record<string, number>;
  total_segmented_customers: number;
  segments: CustomerSegment[];
}

export interface ChurnModelComparison {
  model_name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  confusion_matrix: {
    true_negatives: number;
    false_positives: number;
    false_negatives: number;
    true_positives: number;
  };
}

export interface RiskBandItem {
  risk_band: string;
  customer_count: number;
  share_pct: number;
}

export interface AtRiskVIPCustomer {
  customer_id: string;
  customer_name: string;
  region: string;
  segment: string;
  total_spend: number;
  total_orders: number;
  recency_days: number;
  churn_probability: number;
  risk_band: string;
}

export interface CustomerChurnResponse {
  champion_model: string;
  champion_roc_auc: number;
  business_definition: string;
  total_analyzed_customers: number;
  actual_churn_rate_pct: number;
  model_comparisons: ChurnModelComparison[];
  feature_importances: { feature: string; importance: number }[];
  risk_band_distribution: RiskBandItem[];
  top_at_risk_vip_customers: AtRiskVIPCustomer[];
}

export interface ForecastTimelinePoint {
  year_month: string;
  actual_revenue: number | null;
  predicted_revenue: number | null;
  lower_bound_90ci: number | null;
  upper_bound_90ci: number | null;
  is_forecast: boolean;
}

export interface DemandForecastResponse {
  model_architecture: string;
  validation_metrics: {
    baseline_mape: number;
    champion_mape: number;
    champion_mae: number;
    champion_rmse: number;
  };
  forecast_horizon_months: number;
  forecast_timeline: ForecastTimelinePoint[];
  next_quarter_projected_revenue: number;
  category_forecasts: {
    category_name: string;
    recent_monthly_avg: number;
    projected_monthly_trend: { year_month: string; projected_revenue: number }[];
  }[];
}

export interface BusinessRecommendation {
  id: string;
  category: string;
  priority: string;
  effort: string;
  title: string;
  finding: string;
  recommended_action: string;
  expected_impact: string;
}

export interface AIAnswerResponse {
  question: string;
  tool_called: string;
  answer: string;
  evidence: Record<string, any>;
  interpretation: string;
  recommendation: string;
  caveat: string;
}

export interface DiagnosticFinding {
  type: string;
  severity: 'high' | 'medium' | 'info';
  title: string;
  description: string;
  metric_impact: string;
}
