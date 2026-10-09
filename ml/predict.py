"""
DemandX Market Demand Prediction Inference Module
================================================
Loads the serialized DemandX ML model pipeline (ml/models/demand_model.pkl)
and exposes a clean, reusable `predict_demand` function for backend & API consumption.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from typing import Union, Dict, List

# Re-import DemandXPreprocessor class so joblib deserialization locates class definition
try:
    from train_model import DemandXPreprocessor
except ImportError:
    from ml.train_model import DemandXPreprocessor


def load_demand_model(model_path: str = None) -> dict:
    """
    Loads and returns the trained DemandX model artifact dictionary.
    """
    if model_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'models', 'demand_model.pkl')

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"DemandX trained model file not found at: {model_path}\n"
            "Please run 'python ml/train_model.py' to train and save the model first."
        )

    try:
        artifact = joblib.load(model_path)
        return artifact
    except Exception as e:
        raise RuntimeError(f"Error loading model artifact from {model_path}: {str(e)}")


def predict_demand(
    input_data: Union[Dict, List[Dict], pd.DataFrame],
    model_path: str = None,
    return_float: bool = False
) -> Union[int, List[int], List[float]]:
    """
    Predicts market demand (Units_Sold_Demand) for input product and scenario attributes.

    Parameters:
    -----------
    input_data : Dict, List[Dict], or pd.DataFrame
        Product scenario attributes (e.g. Product_Name, Category, Brand, City, State,
        Price, Temperature, Weather, Season, etc.)
    model_path : str, optional
        Path to demand_model.pkl. If None, resolves to ml/models/demand_model.pkl.
    return_float : bool, optional
        If True, returns raw floating-point predictions. Defaults to rounded integers.

    Returns:
    --------
    Predicted demand (int, float, or list of ints/floats).
    """
    # 1. Load model artifact
    artifact = load_demand_model(model_path)
    preprocessor: DemandXPreprocessor = artifact['preprocessor']
    model = artifact['model']

    # 2. Format input data into DataFrame
    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])
        single_input = True
    elif isinstance(input_data, list):
        df_input = pd.DataFrame(input_data)
        single_input = False
    elif isinstance(input_data, pd.DataFrame):
        df_input = input_data.copy()
        single_input = len(df_input) == 1
    else:
        raise ValueError("input_data must be a dict, list of dicts, or pandas DataFrame.")

    if df_input.empty:
        raise ValueError("Provided input_data is empty.")

    # 3. Preprocess features using saved preprocessor
    try:
        feature_matrix = preprocessor.transform(df_input)
    except Exception as e:
        raise ValueError(f"Error preprocessing input features: {str(e)}")

    # 4. Construct DMatrix and predict
    dmatrix = xgb.DMatrix(feature_matrix, feature_names=preprocessor.feature_names_)
    raw_predictions = model.predict(dmatrix)

    # 5. Post-process predictions (demand units cannot be negative)
    clipped_preds = np.clip(raw_predictions, a_min=0, a_max=None)

    if not return_float:
        final_preds = [int(round(val)) for val in clipped_preds]
    else:
        final_preds = [float(val) for val in clipped_preds]

    if single_input:
        return final_preds[0]
    return final_preds


# =====================================================================
# DEMO & SAMPLE PREDICTION
# =====================================================================
if __name__ == '__main__':
    print("=" * 70)
    print("           DemandX AI -- Real-Time Market Demand Prediction           ")
    print("=" * 70)

    # Load model info
    try:
        art = load_demand_model()
        print(f" Loaded Champion Model: {art['model_name']}")
        print(f" Training R² Score:     {art['best_metrics']['R2']:.4f}")
        print(f" Training MAE:          {art['best_metrics']['MAE']:.4f} units")
        print(f" Model Trained At:      {art['trained_at']}")
        print("-" * 70)
    except Exception as err:
        print(f"[!] {err}")
        sys.exit(1)

    # Sample Test Scenarios across FMCG products & Indian cities
    sample_scenarios = [
        {
            "scenario_name": "Fortune Sunflower Oil 1L -- Monsoon High Demand (Bengaluru)",
            "Product_Name": "Fortune Sunflower Oil 1L",
            "Category": "Cooking Oil",
            "Brand": "Adani Wilmar",
            "State": "Karnataka",
            "City": "Bengaluru",
            "Region": "South",
            "City_Tier": "Metro",
            "Season": "Monsoon",
            "Festival_Event": "None",
            "Weather": "Rainy",
            "Promotion": "Yes",
            "Day": "Friday",
            "Month": 7,
            "Year": 2026,
            "Week": 28,
            "Weekend": 0,
            "Holiday": 0,
            "Temperature_C": 24.5,
            "Rainfall_mm": 12.5,
            "Humidity_pct": 85,
            "Selling_Price_INR": 145.0,
            "MRP_INR": 155.0,
            "Discount_pct": 6,
            "Competitor_Price_INR": 150.0,
            "Opening_Stock": 200,
            "Customer_Footfall": 850,
            "Lead_Time_Days": 4,
            "Prev_Day_Demand": 62,
            "7_Day_Avg_Demand": 58.4,
            "30_Day_Avg_Demand": 54.2
        },
        {
            "scenario_name": "Amul Taaza Milk 1L -- Holiday Morning Peak (Hyderabad)",
            "Product_Name": "Amul Taaza Milk 1L",
            "Category": "Dairy",
            "Brand": "Amul",
            "State": "Telangana",
            "City": "Hyderabad",
            "Region": "South",
            "City_Tier": "Metro",
            "Season": "Summer",
            "Festival_Event": "Ugadi",
            "Weather": "Clear",
            "Promotion": "No",
            "Day": "Sunday",
            "Month": 4,
            "Year": 2026,
            "Week": 14,
            "Weekend": 1,
            "Holiday": 1,
            "Temperature_C": 36.0,
            "Rainfall_mm": 0.0,
            "Humidity_pct": 45,
            "Selling_Price_INR": 58.0,
            "MRP_INR": 58.0,
            "Discount_pct": 0,
            "Competitor_Price_INR": 58.0,
            "Opening_Stock": 350,
            "Customer_Footfall": 1200,
            "Lead_Time_Days": 1,
            "Prev_Day_Demand": 140,
            "7_Day_Avg_Demand": 125.0,
            "30_Day_Avg_Demand": 118.0
        },
        {
            "scenario_name": "Aashirvaad Atta 5kg -- Festive Stock Up (Patna)",
            "Product_Name": "Aashirvaad Atta 5kg",
            "Category": "Staples",
            "Brand": "ITC",
            "State": "Bihar",
            "City": "Patna",
            "Region": "East",
            "City_Tier": "Metro",
            "Season": "Post-Monsoon",
            "Festival_Event": "Chhath Puja",
            "Weather": "Clear",
            "Promotion": "Yes",
            "Day": "Wednesday",
            "Month": 11,
            "Year": 2026,
            "Week": 45,
            "Weekend": 0,
            "Holiday": 1,
            "Temperature_C": 22.0,
            "Rainfall_mm": 0.0,
            "Humidity_pct": 50,
            "Selling_Price_INR": 295.0,
            "MRP_INR": 310.0,
            "Discount_pct": 5,
            "Competitor_Price_INR": 305.0,
            "Opening_Stock": 180,
            "Customer_Footfall": 950,
            "Lead_Time_Days": 3,
            "Prev_Day_Demand": 88,
            "7_Day_Avg_Demand": 82.5,
            "30_Day_Avg_Demand": 76.0
        }
    ]

    print(" Running Sample Product Scenario Predictions:")
    print("-" * 70)

    for idx, sc in enumerate(sample_scenarios, 1):
        name = sc.pop("scenario_name")
        predicted_demand = predict_demand(sc)
        print(f" [{idx}] {name}")
        print(f"     • Product: {sc['Product_Name']} ({sc['City']}, {sc['State']})")
        print(f"     • Key Conditions: {sc['Season']} | {sc['Weather']} | Discount: {sc['Discount_pct']}%")
        print(f"     • PREDICTED MARKET DEMAND: {predicted_demand} units")
        print("-" * 70)

    print(" Sample prediction inference test completed successfully!\n")
