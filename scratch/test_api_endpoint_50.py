import os
import sys
import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Try port 8001 first, then 8000
API_URLS = ["http://127.0.0.1:8001/api/predict-demand", "http://127.0.0.1:8000/api/predict-demand"]

def test_fastapi_endpoint():
    excel_path = os.path.join(BASE_DIR, 'ml', 'data', 'DemandX_India_Datasets_10000 final.xlsx')
    df_products = pd.read_excel(excel_path, sheet_name='Product_Master')
    
    # Determine active endpoint
    active_url = None
    for url in API_URLS:
        try:
            health_url = url.replace('/predict-demand', '/health')
            r = requests.get(health_url, timeout=2)
            if r.status_code == 200:
                active_url = url
                print(f"Found active FastAPI server at: {active_url}")
                break
        except Exception:
            continue
            
    if not active_url:
        print("FastAPI server not currently running on 8001 or 8000. Testing backend main.py directly via TestClient...")
        from fastapi.testclient import TestClient
        from backend.main import app
        client = TestClient(app)
        
        success_count = 0
        errors = []
        for idx, row in df_products.iterrows():
            p_name = row['Product_Name']
            cat = row['Category']
            brand = row['Brand']
            mrp = row['MRP_INR']
            
            payload = {
                "Product_Name": p_name,
                "Category": cat,
                "Brand": brand,
                "State": "Karnataka",
                "City": "Bengaluru",
                "Region": "South",
                "City_Tier": "Metro",
                "Season": "Monsoon",
                "Festival_Event": "None",
                "Weather": "Clear",
                "Promotion": "Yes",
                "Day": "Monday",
                "Month": 7,
                "Year": 2026,
                "Week": 28,
                "Weekend": 0,
                "Holiday": 0,
                "Temperature_C": 25.0,
                "Rainfall_mm": 0.0,
                "Humidity_pct": 65,
                "Selling_Price_INR": float(mrp),
                "MRP_INR": float(mrp),
                "Discount_pct": 0,
                "Competitor_Price_INR": float(mrp) * 1.05,
                "Opening_Stock": 100,
                "Customer_Footfall": 700,
                "Lead_Time_Days": 3,
                "Prev_Day_Demand": 50.0,
                "7_Day_Avg_Demand": 48.0,
                "30_Day_Avg_Demand": 45.0
            }
            
            res = client.post("/api/predict-demand", json=payload)
            if res.status_code == 200:
                data = res.json()
                assert data["success"] is True
                assert "predicted_demand" in data
                success_count += 1
                print(f"[{success_count}/50] API 200 OK: '{p_name}' -> demand={data['predicted_demand']} units, level={data['demand_level']}")
            else:
                errors.append((p_name, res.text))
                print(f"[FAIL] HTTP {res.status_code} for {p_name}: {res.text}")
                
        print(f"\nTestClient Summary: {success_count}/50 API predictions succeeded. Errors: {len(errors)}")
        return

    # If server is running live over HTTP
    success_count = 0
    errors = []
    for idx, row in df_products.iterrows():
        p_name = row['Product_Name']
        cat = row['Category']
        brand = row['Brand']
        mrp = row['MRP_INR']
        
        payload = {
            "Product_Name": p_name,
            "Category": cat,
            "Brand": brand,
            "State": "Karnataka",
            "City": "Bengaluru",
            "Region": "South",
            "City_Tier": "Metro",
            "Season": "Monsoon",
            "Festival_Event": "None",
            "Weather": "Clear",
            "Promotion": "Yes",
            "Day": "Monday",
            "Month": 7,
            "Year": 2026,
            "Week": 28,
            "Weekend": 0,
            "Holiday": 0,
            "Temperature_C": 25.0,
            "Rainfall_mm": 0.0,
            "Humidity_pct": 65,
            "Selling_Price_INR": float(mrp),
            "MRP_INR": float(mrp),
            "Discount_pct": 0,
            "Competitor_Price_INR": float(mrp) * 1.05,
            "Opening_Stock": 100,
            "Customer_Footfall": 700,
            "Lead_Time_Days": 3,
            "Prev_Day_Demand": 50.0,
            "7_Day_Avg_Demand": 48.0,
            "30_Day_Avg_Demand": 45.0
        }
        
        res = requests.post(active_url, json=payload, timeout=5)
        if res.status_code == 200:
            data = res.json()
            assert data["success"] is True
            assert "predicted_demand" in data
            success_count += 1
            print(f"[{success_count}/50] Live HTTP 200 OK: '{p_name}' -> demand={data['predicted_demand']} units")
        else:
            errors.append((p_name, res.text))
            print(f"[FAIL] HTTP {res.status_code} for {p_name}: {res.text}")

    print(f"\nLive HTTP Server Summary: {success_count}/50 API predictions succeeded. Errors: {len(errors)}")

if __name__ == '__main__':
    test_fastapi_endpoint()
