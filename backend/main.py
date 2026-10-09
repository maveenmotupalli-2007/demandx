"""
DemandX AI — FastAPI Backend Service
====================================
Serves real-time market demand predictions using the trained XGBoost model pipeline
(ml/models/demand_model.pkl). Provides REST API endpoints for frontend consumption,
health monitoring, and automatic Swagger documentation (/docs).
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from typing import Optional, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict

# Ensure 'ml' directory is in python path to load DemandXPreprocessor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, 'ml')
if ML_DIR not in sys.path:
    sys.path.insert(0, ML_DIR)

try:
    from train_model import DemandXPreprocessor
    from predict import predict_demand, load_demand_model
except ImportError:
    from ml.train_model import DemandXPreprocessor
    from ml.predict import predict_demand, load_demand_model


# Initialize FastAPI Application
app = FastAPI(
    title="DemandX Intelligence API",
    description="AI-Powered Market Demand Prediction API for FMCG & Supply Chain Intelligence across India",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware for Frontend React App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Model Cache
MODEL_ARTIFACT = None


@app.on_event("startup")
def load_ml_model():
    """Loads the pre-trained demand model artifact into memory on server startup."""
    global MODEL_ARTIFACT
    model_path = os.path.join(BASE_DIR, 'ml', 'models', 'demand_model.pkl')
    
    if not os.path.exists(model_path):
        raise RuntimeError(
            f"Trained model file not found at: {model_path}. "
            "Please run 'python ml/train_model.py' to generate the model first."
        )

    try:
        MODEL_ARTIFACT = load_demand_model(model_path)
        print(f" DemandX ML Model loaded! Model: {MODEL_ARTIFACT['model_name']} (R² = {MODEL_ARTIFACT['best_metrics']['R2']:.4f})")
    except Exception as err:
        raise RuntimeError(f"Failed to load ML model artifact: {str(err)}")


# =====================================================================
# REQUEST & RESPONSE PYDANTIC SCHEMAS
# =====================================================================
class DemandPredictionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Product_Name: str = Field(default="Fortune Sunflower Oil 1L", json_schema_extra={"example": "Fortune Sunflower Oil 1L"})
    Category: str = Field(default="Cooking Oil", json_schema_extra={"example": "Cooking Oil"})
    Brand: str = Field(default="Adani Wilmar", json_schema_extra={"example": "Adani Wilmar"})
    State: str = Field(default="Karnataka", json_schema_extra={"example": "Karnataka"})
    City: str = Field(default="Bengaluru", json_schema_extra={"example": "Bengaluru"})
    Region: str = Field(default="South", json_schema_extra={"example": "South"})
    City_Tier: str = Field(default="Metro", json_schema_extra={"example": "Metro"})
    Season: str = Field(default="Monsoon", json_schema_extra={"example": "Monsoon"})
    Festival_Event: str = Field(default="None", json_schema_extra={"example": "None"})
    Weather: str = Field(default="Clear", json_schema_extra={"example": "Clear"})
    Promotion: str = Field(default="No", json_schema_extra={"example": "No"})
    Day: str = Field(default="Monday", json_schema_extra={"example": "Monday"})
    Month: int = Field(default=7, ge=1, le=12, json_schema_extra={"example": 7})
    Year: int = Field(default=2026, ge=2024, le=2030, json_schema_extra={"example": 2026})
    Week: int = Field(default=28, ge=1, le=53, json_schema_extra={"example": 28})
    Weekend: int = Field(default=0, ge=0, le=1, json_schema_extra={"example": 0})
    Holiday: int = Field(default=0, ge=0, le=1, json_schema_extra={"example": 0})
    Temperature_C: float = Field(default=25.0, json_schema_extra={"example": 25.0})
    Rainfall_mm: float = Field(default=0.0, json_schema_extra={"example": 0.0})
    Humidity_pct: int = Field(default=65, ge=0, le=100, json_schema_extra={"example": 65})
    Selling_Price_INR: float = Field(default=145.0, json_schema_extra={"example": 145.0})
    MRP_INR: float = Field(default=155.0, json_schema_extra={"example": 155.0})
    Discount_pct: int = Field(default=6, ge=0, le=100, json_schema_extra={"example": 6})
    Competitor_Price_INR: float = Field(default=150.0, json_schema_extra={"example": 150.0})
    Opening_Stock: int = Field(default=100, ge=0, json_schema_extra={"example": 100})
    Customer_Footfall: int = Field(default=650, ge=0, json_schema_extra={"example": 650})
    Lead_Time_Days: int = Field(default=4, ge=1, json_schema_extra={"example": 4})
    Prev_Day_Demand: float = Field(default=55.0, ge=0, json_schema_extra={"example": 55.0})
    
    # Aliased fields for keys starting with numbers
    Avg_Demand_7_Day: float = Field(default=52.0, alias="7_Day_Avg_Demand", ge=0, json_schema_extra={"example": 52.0})
    Avg_Demand_30_Day: float = Field(default=50.0, alias="30_Day_Avg_Demand", ge=0, json_schema_extra={"example": 50.0})

    def to_ml_dict(self) -> dict:
        """Converts model fields to exact dict keys required by ML preprocessor."""
        d = self.model_dump(by_alias=True)
        return d


class DemandPredictionResponse(BaseModel):
    success: bool
    predicted_demand: int
    demand_level: str
    recommended_stock: int
    recommended_reorder_quantity: int
    product: Optional[str] = None
    city: Optional[str] = None


class HealthCheckResponse(BaseModel):
    status: str
    model: str
    r2: float


# =====================================================================
# API ENDPOINTS
# =====================================================================
@app.get("/api/health", response_model=HealthCheckResponse, summary="Check Backend & Model Health")
def health_check():
    """
    Health check endpoint returning system status and loaded model metrics.
    """
    if MODEL_ARTIFACT is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML Model artifact is not loaded."
        )

    return HealthCheckResponse(
        status="ok",
        model=MODEL_ARTIFACT.get("model_name", "XGBoost Regressor"),
        r2=float(MODEL_ARTIFACT.get("best_metrics", {}).get("R2", 0.9626))
    )


@app.post("/api/predict-demand", response_model=DemandPredictionResponse, summary="Predict Market Demand")
def predict_market_demand(payload: DemandPredictionRequest):
    """
    Predicts market demand (Units_Sold_Demand) using the trained XGBoost ML pipeline.
    Calculates demand level, recommended stock buffer, and reorder quantities.
    """
    try:
        input_dict = payload.to_ml_dict()
        model_path = os.path.join(BASE_DIR, 'ml', 'models', 'demand_model.pkl')

        # Run inference through pipeline
        predicted_demand_val = predict_demand(input_dict, model_path=model_path, return_float=False)
        predicted_demand = int(predicted_demand_val)

        # Calculate Demand Level (LOW < 50, MEDIUM 50-150, HIGH > 150)
        if predicted_demand < 50:
            demand_level = "LOW"
        elif predicted_demand <= 150:
            demand_level = "MEDIUM"
        else:
            demand_level = "HIGH"

        # Calculate Recommended Stock (with 15% safety buffer)
        recommended_stock = int(round(predicted_demand * 1.15))

        # Calculate Recommended Reorder Quantity (Opening Stock subtracted, non-negative)
        opening_stock = payload.Opening_Stock
        recommended_reorder_quantity = max(0, recommended_stock - opening_stock)

        return DemandPredictionResponse(
            success=True,
            predicted_demand=predicted_demand,
            demand_level=demand_level,
            recommended_stock=recommended_stock,
            recommended_reorder_quantity=recommended_reorder_quantity,
            product=payload.Product_Name,
            city=payload.City
        )

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction Error: {str(err)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
