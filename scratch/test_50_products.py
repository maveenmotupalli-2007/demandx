import os
import sys
import pandas as pd
import json

# Add project root and ml directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'ml'))

from ml.predict import predict_demand

def test_all_50_products():
    excel_path = os.path.join(BASE_DIR, 'ml', 'data', 'DemandX_India_Datasets_10000 final.xlsx')
    df_products = pd.read_excel(excel_path, sheet_name='Product_Master')
    
    print(f"Loaded {len(df_products)} products from Product_Master.")
    assert len(df_products) == 50, f"Expected 50 products, found {len(df_products)}"
    
    ten_required_test_products = [
        "Amul Taaza Milk 1L",
        "Aashirvaad Atta 5kg",
        "Tata Salt 1kg",
        "Fortune Sunflower Oil 1L",
        "Tata Tea Gold 500g",
        "Parle-G Biscuits 800g",
        "Coca-Cola 750ml",
        "Thums Up 750ml",
        "Maggi Noodles 280g",
        "Surf Excel Matic 2kg"
    ]
    
    successful_count = 0
    errors = []
    results_summary = []
    
    for idx, row in df_products.iterrows():
        p_name = row['Product_Name']
        cat = row['Category']
        brand = row['Brand']
        mrp = row['MRP_INR']
        
        sample_payload = {
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
        
        try:
            pred_demand = predict_demand(sample_payload)
            successful_count += 1
            is_required = p_name in ten_required_test_products
            tag = " [REQUIRED TEST PRODUCT]" if is_required else ""
            results_summary.append({
                "product": p_name,
                "category": cat,
                "brand": brand,
                "mrp": mrp,
                "predicted_demand": pred_demand,
                "is_required_test": is_required
            })
            print(f"[{successful_count}/50] Success: '{p_name}' -> Predicted Demand = {pred_demand} units{tag}")
        except Exception as e:
            errors.append((p_name, str(e)))
            print(f"[FAIL] Error predicting for '{p_name}': {e}")

    print("\n" + "=" * 60)
    print(f"SUMMARY: {successful_count}/50 products successfully predicted.")
    print(f"Errors count: {len(errors)}")
    print("=" * 60)
    
    # Check 10 required products explicitly
    print("\nChecking 10 specific test products required by prompt:")
    tested_required = [r for r in results_summary if r["is_required_test"]]
    for item in tested_required:
        print(f" • {item['product']:<30} | Category: {item['category']:<15} | MRP: ₹{item['mrp']:<5} | Predicted Demand: {item['predicted_demand']} units")
    
    assert len(tested_required) == 10, f"Expected 10 required test products, found {len(tested_required)}"
    print("\nAll 10 required products verified successfully!")

if __name__ == '__main__':
    test_all_50_products()
