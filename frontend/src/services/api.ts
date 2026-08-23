import axios from 'axios';
import {
  ExecutiveSummary,
  MonthlyTrend,
  RegionalMetric,
  CategoryMetric,
  ProductMetric,
  SegmentationResponse,
  CustomerChurnResponse,
  DemandForecastResponse,
  BusinessRecommendation,
  AIAnswerResponse,
  DiagnosticFinding
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Executive Dashboard
  getExecutiveSummary: async (): Promise<ExecutiveSummary> => {
    const res = await client.get<ExecutiveSummary>('/dashboard/summary');
    return res.data;
  },

  // Sales Trends
  getSalesTrends: async (startDate?: string, endDate?: string): Promise<MonthlyTrend[]> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    const res = await client.get<MonthlyTrend[]>(`/sales/trends?${params.toString()}`);
    return res.data;
  },

  // Regional Sales
  getRegionalSales: async (): Promise<RegionalMetric[]> => {
    const res = await client.get<RegionalMetric[]>('/sales/regions');
    return res.data;
  },

  // Category Sales
  getCategorySales: async (): Promise<CategoryMetric[]> => {
    const res = await client.get<CategoryMetric[]>('/sales/categories');
    return res.data;
  },

  // Products
  getTopProducts: async (limit = 10, sortBy = 'revenue'): Promise<ProductMetric[]> => {
    const res = await client.get<ProductMetric[]>(`/products/top?limit=${limit}&sort_by=${sortBy}`);
    return res.data;
  },

  getUnderperformingProducts: async (limit = 10): Promise<ProductMetric[]> => {
    const res = await client.get<ProductMetric[]>(`/products/underperforming?limit=${limit}`);
    return res.data;
  },

  // Customer Segmentation
  getCustomerSegments: async (): Promise<SegmentationResponse> => {
    const res = await client.get<SegmentationResponse>('/customers/segments');
    return res.data;
  },

  // Customer Churn
  getCustomerChurn: async (): Promise<CustomerChurnResponse> => {
    const res = await client.get<CustomerChurnResponse>('/customers/churn');
    return res.data;
  },

  // Forecasting
  getDemandForecast: async (): Promise<DemandForecastResponse> => {
    const res = await client.get<DemandForecastResponse>('/forecast');
    return res.data;
  },

  // Prescriptive Recommendations
  getRecommendations: async (): Promise<BusinessRecommendation[]> => {
    const res = await client.get<BusinessRecommendation[]>('/recommendations');
    return res.data;
  },

  // Diagnostics
  getDiagnostics: async (): Promise<{ diagnostic_status: string; total_findings: number; findings: DiagnosticFinding[] }> => {
    const res = await client.get('/diagnostics');
    return res.data;
  },

  // GenAI Business Analyst
  askAIAnalyst: async (question: string): Promise<AIAnswerResponse> => {
    const res = await client.post<AIAnswerResponse>('/ai/ask', { question });
    return res.data;
  },
};
