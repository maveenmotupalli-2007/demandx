/**
 * DemandX FastAPI Backend Service Client
 * Connects React frontend directly to FastAPI backend ML prediction endpoints.
 */

export interface DemandPredictionPayload {
  Product_Name: string;
  Category: string;
  Brand: string;
  State: string;
  City: string;
  Region: string;
  City_Tier: string;
  Season: string;
  Festival_Event?: string;
  Weather?: string;
  Promotion?: string;
  Day?: string;
  Month?: number;
  Year?: number;
  Week?: number;
  Weekend?: number;
  Holiday?: number;
  Temperature_C?: number;
  Rainfall_mm?: number;
  Humidity_pct?: number;
  Selling_Price_INR: number;
  MRP_INR: number;
  Discount_pct?: number;
  Competitor_Price_INR?: number;
  Opening_Stock: number;
  Customer_Footfall?: number;
  Lead_Time_Days?: number;
  Prev_Day_Demand?: number;
  '7_Day_Avg_Demand'?: number;
  '30_Day_Avg_Demand'?: number;
}

export interface DemandPredictionResult {
  success: boolean;
  predicted_demand: number;
  demand_level: 'LOW' | 'MEDIUM' | 'HIGH';
  recommended_stock: number;
  recommended_reorder_quantity: number;
  product?: string;
  city?: string;
  is_fallback?: boolean;
}

export interface HealthStatus {
  status: string;
  model: string;
  r2: number;
}

// Configurable API base URL from environment variable VITE_API_BASE_URL or fallback
const ENV_URL = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || 'http://127.0.0.1:8001';
const CLEAN_BASE = ENV_URL.replace(/\/$/, '');
export const API_BASE_URL = CLEAN_BASE.endsWith('/api') ? CLEAN_BASE : `${CLEAN_BASE}/api`;

/**
 * Checks backend health status and loaded model metrics.
 */
export async function getBackendHealth(): Promise<HealthStatus | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn('DemandX Backend API health check failed:', err);
    return null;
  }
}

/**
 * Intelligent client-side fallback calculation when FastAPI backend is offline.
 */
function calculateFallbackPrediction(payload: DemandPredictionPayload): DemandPredictionResult {
  const baseDemand = payload.Prev_Day_Demand || payload['7_Day_Avg_Demand'] || 55;
  const priceRatio = payload.MRP_INR > 0 ? (payload.Selling_Price_INR / payload.MRP_INR) : 1;
  const priceFactor = 1 + (1 - priceRatio) * 0.4;
  const footfallFactor = payload.Customer_Footfall ? Math.min(1.5, Math.max(0.6, payload.Customer_Footfall / 600)) : 1;
  
  let eventFactor = 1.0;
  if (payload.Festival_Event && payload.Festival_Event !== 'None') {
    eventFactor = 1.25;
  }
  if (payload.Promotion === 'Yes') {
    eventFactor *= 1.15;
  }

  const calculated = Math.round(baseDemand * priceFactor * footfallFactor * eventFactor);
  const predicted = Math.max(10, calculated);

  let level: 'LOW' | 'MEDIUM' | 'HIGH' = 'MEDIUM';
  if (predicted < 50) level = 'LOW';
  else if (predicted > 150) level = 'HIGH';

  const recStock = Math.round(predicted * 1.15);
  const reorder = Math.max(0, recStock - (payload.Opening_Stock || 0));

  return {
    success: true,
    predicted_demand: predicted,
    demand_level: level,
    recommended_stock: recStock,
    recommended_reorder_quantity: reorder,
    product: payload.Product_Name,
    city: payload.City,
    is_fallback: true
  };
}

/**
 * Invokes trained ML model prediction API endpoint (POST /api/predict-demand).
 * Falls back to intelligent estimator if FastAPI backend server is unreachable.
 */
export async function fetchDemandPrediction(
  payload: DemandPredictionPayload
): Promise<DemandPredictionResult> {
  try {
    const res = await fetch(`${API_BASE_URL}/predict-demand`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`API error HTTP ${res.status}`);
    }

    const data: DemandPredictionResult = await res.json();
    return { ...data, is_fallback: false };
  } catch (err) {
    console.warn('DemandX AI Backend prediction API unreachable, using fallback estimator:', err);
    return calculateFallbackPrediction(payload);
  }
}
