"""
Controlled Inference Evaluation Experiment for DemandX ML Model
================================================================
This script runs inference using the serialized DemandX XGBoost model pipeline
(ml/models/demand_model.pkl) against the full DemandX dataset (10,000 rows).
It calculates detailed evaluation scores across:
  - Overall Full Dataset (10,000 rows)
  - Train Set (80% chronological split = 8,000 rows)
  - Test Set / Unseen Holdout (20% chronological split = 2,000 rows)
  - Per-Category Breakdowns
  - Selected Product Breakdowns
  - Error Percentiles & Threshold Accuracy
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
import xgboost as xgb

# Ensure project root and ml directory are in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ML_DIR = os.path.join(BASE_DIR, 'ml')
if ML_DIR not in sys.path:
    sys.path.insert(0, ML_DIR)

from train_model import DemandXPreprocessor
from predict import load_demand_model

def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Computes comprehensive regression metrics."""
    errors = y_true - y_pred
    abs_errors = np.abs(errors)
    sq_errors = errors ** 2
    
    mae = float(np.mean(abs_errors))
    mse = float(np.mean(sq_errors))
    rmse = float(np.sqrt(mse))
    
    ss_res = np.sum(sq_errors)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = float(1.0 - (ss_res / ss_tot)) if ss_tot != 0 else 0.0
    
    # WAPE (Weighted Absolute Percentage Error)
    wape = float(np.sum(abs_errors) / np.sum(y_true) * 100) if np.sum(y_true) != 0 else 0.0
    
    # MAPE (for non-zero true values)
    non_zero_mask = y_true > 0
    mape = float(np.mean(abs_errors[non_zero_mask] / y_true[non_zero_mask]) * 100) if np.any(non_zero_mask) else 0.0
    
    # Percentiles
    median_abs_err = float(np.median(abs_errors))
    p90_abs_err = float(np.percentile(abs_errors, 90))
    p95_abs_err = float(np.percentile(abs_errors, 95))
    p99_abs_err = float(np.percentile(abs_errors, 99))
    max_abs_err = float(np.max(abs_errors))
    
    # Threshold Accuracies
    acc_within_3 = float(np.mean(abs_errors <= 3) * 100)
    acc_within_5 = float(np.mean(abs_errors <= 5) * 100)
    acc_within_10 = float(np.mean(abs_errors <= 10) * 100)
    acc_within_15 = float(np.mean(abs_errors <= 15) * 100)
    
    return {
        "sample_count": len(y_true),
        "mean_actual_demand": float(np.mean(y_true)),
        "mean_predicted_demand": float(np.mean(y_pred)),
        "MAE": mae,
        "RMSE": rmse,
        "MSE": mse,
        "R2": r2,
        "WAPE_pct": wape,
        "MAPE_pct": mape,
        "median_abs_error": median_abs_err,
        "p90_abs_error": p90_abs_err,
        "p95_abs_error": p95_abs_err,
        "p99_abs_error": p99_abs_err,
        "max_abs_error": max_abs_err,
        "accuracy_within_3_units_pct": acc_within_3,
        "accuracy_within_5_units_pct": acc_within_5,
        "accuracy_within_10_units_pct": acc_within_10,
        "accuracy_within_15_units_pct": acc_within_15
    }

def run_experiment():
    print("=" * 80)
    print("      DemandX AI -- Controlled Model Inference & Evaluation Experiment     ")
    print("=" * 80)
    start_time = time.time()
    
    # 1. Load Model Artifact
    model_path = os.path.join(ML_DIR, 'models', 'demand_model.pkl')
    print(f"[*] Loading model artifact from: {model_path}")
    artifact = load_demand_model(model_path)
    model = artifact['model']
    preprocessor: DemandXPreprocessor = artifact['preprocessor']
    print(f"[+] Model Algorithm: {artifact['model_name']}")
    print(f"[+] Model Trained At: {artifact['trained_at']}")
    
    # 2. Load Dataset
    excel_path = os.path.join(ML_DIR, 'data', 'DemandX_India_Datasets_10000 final.xlsx')
    print(f"[*] Loading dataset from: {excel_path}")
    df = pd.read_excel(excel_path, sheet_name='Demand_Model')
    print(f"[+] Dataset Loaded: {len(df)} rows x {len(df.columns)} columns")
    
    # Target column
    target_col = 'Units_Sold_Demand'
    y_actual = df[target_col].values.astype(np.float32)
    
    # Sort chronologically if Date present (matching training pipeline logic)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        y_actual = df[target_col].values.astype(np.float32)
    
    # 3. Transform Features & Run Model Inference
    print("\n[*] Preprocessing feature matrix through DemandX preprocessor...")
    feature_matrix = preprocessor.transform(df)
    dmatrix = xgb.DMatrix(feature_matrix, feature_names=preprocessor.feature_names_)
    
    print("[*] Executing XGBoost inference on 10,000 samples...")
    inf_start = time.time()
    raw_preds = model.predict(dmatrix)
    inf_duration = time.time() - inf_start
    
    # Clip negative predictions to zero
    y_pred_float = np.clip(raw_preds, a_min=0, a_max=None)
    y_pred_int = np.round(y_pred_float)
    
    # Store predictions in dataframe for slice analysis
    df['Predicted_Demand_Float'] = y_pred_float
    df['Predicted_Demand_Int'] = y_pred_int
    df['Absolute_Error'] = np.abs(df[target_col] - df['Predicted_Demand_Int'])
    
    # 4. Chronological Train / Test Slices (80 / 20 split)
    split_idx = int(len(df) * 0.8)
    
    y_true_full = df[target_col].values
    y_pred_full = df['Predicted_Demand_Int'].values
    
    y_true_train = df[target_col].iloc[:split_idx].values
    y_pred_train = df['Predicted_Demand_Int'].iloc[:split_idx].values
    
    y_true_test = df[target_col].iloc[split_idx:].values
    y_pred_test = df['Predicted_Demand_Int'].iloc[split_idx:].values
    
    # Calculate Overall Scores
    overall_metrics = calculate_metrics(y_true_full, y_pred_full)
    train_metrics = calculate_metrics(y_true_train, y_pred_train)
    test_metrics = calculate_metrics(y_true_test, y_pred_test)
    
    # 5. Category-wise Scores
    cat_metrics = {}
    for cat, group in df.groupby('Category'):
        y_t = group[target_col].values
        y_p = group['Predicted_Demand_Int'].values
        cat_metrics[cat] = calculate_metrics(y_t, y_p)
        
    # 6. Sample Product-wise Scores (Top 10 required products)
    required_products = [
        "Amul Taaza Milk 1L", "Aashirvaad Atta 5kg", "Tata Salt 1kg",
        "Fortune Sunflower Oil 1L", "Tata Tea Gold 500g", "Parle-G Biscuits 800g",
        "Coca-Cola 750ml", "Thums Up 750ml", "Maggi Noodles 280g", "Surf Excel Matic 2kg"
    ]
    
    prod_metrics = {}
    for prod in required_products:
        group = df[df['Product_Name'] == prod]
        if not group.empty:
            y_t = group[target_col].values
            y_p = group['Predicted_Demand_Int'].values
            prod_metrics[prod] = calculate_metrics(y_t, y_p)
            
    # 7. Output Experiment Results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    
    # Save CSV with predictions
    csv_path = os.path.join(output_dir, 'inference_results.csv')
    df.to_csv(csv_path, index=False)
    
    # Save JSON report
    report_data = {
        "experiment_name": "Controlled Inference Evaluation",
        "model_name": artifact['model_name'],
        "inference_latency_ms_total": float(inf_duration * 1000),
        "inference_latency_ms_per_sample": float(inf_duration * 1000 / len(df)),
        "overall_full_dataset": overall_metrics,
        "train_set_80pct": train_metrics,
        "test_set_20pct": test_metrics,
        "category_breakdown": cat_metrics,
        "required_products_breakdown": prod_metrics
    }
    
    json_path = os.path.join(output_dir, 'experiment_report.json')
    with open(json_path, 'w') as f:
        json.dump(report_data, f, indent=2)
        
    elapsed = time.time() - start_time
    
    # Print Executive Summary
    print("\n" + "=" * 80)
    print("                     CONTROLLED INFERENCE EXPERIMENT REPORT                ")
    print("=" * 80)
    print(f" Total Samples Evaluated:  {len(df):,} rows")
    print(f" Total Inference Time:     {inf_duration*1000:.2f} ms ({inf_duration*1000/len(df):.4f} ms/sample)")
    print(f" Exported Predictions:     {csv_path}")
    print(f" Exported JSON Metrics:    {json_path}")
    print("-" * 80)
    print(f" {'Data Subset':<22} | {'Samples':<8} | {'MAE':<8} | {'RMSE':<8} | {'R² Score':<8} | {'WAPE %':<8}")
    print("-" * 80)
    print(f" {'Full Dataset (100%)':<22} | {overall_metrics['sample_count']:<8} | {overall_metrics['MAE']:<8.4f} | {overall_metrics['RMSE']:<8.4f} | {overall_metrics['R2']:<8.4f} | {overall_metrics['WAPE_pct']:<8.2f}%")
    print(f" {'Train Split (80%)':<22} | {train_metrics['sample_count']:<8} | {train_metrics['MAE']:<8.4f} | {train_metrics['RMSE']:<8.4f} | {train_metrics['R2']:<8.4f} | {train_metrics['WAPE_pct']:<8.2f}%")
    print(f" {'Test Split (20% Holdout)':<22} | {test_metrics['sample_count']:<8} | {test_metrics['MAE']:<8.4f} | {test_metrics['RMSE']:<8.4f} | {test_metrics['R2']:<8.4f} | {test_metrics['WAPE_pct']:<8.2f}%")
    print("=" * 80)
    
    print("\n[+] ERROR DISTRIBUTION & TOLERANCE ACCURACY (Full Dataset):")
    print(f"   - Median Absolute Error:     {overall_metrics['median_abs_error']:.2f} units")
    print(f"   - P90 Absolute Error:        {overall_metrics['p90_abs_error']:.2f} units")
    print(f"   - P95 Absolute Error:        {overall_metrics['p95_abs_error']:.2f} units")
    print(f"   - Max Absolute Error:        {overall_metrics['max_abs_error']:.2f} units")
    print(f"   - Accuracy within ±3 units:   {overall_metrics['accuracy_within_3_units_pct']:.2f}%")
    print(f"   - Accuracy within ±5 units:   {overall_metrics['accuracy_within_5_units_pct']:.2f}%")
    print(f"   - Accuracy within ±10 units:  {overall_metrics['accuracy_within_10_units_pct']:.2f}%")
    print(f"   - Accuracy within ±15 units:  {overall_metrics['accuracy_within_15_units_pct']:.2f}%")

    print("\n[+] CATEGORY BREAKDOWN:")
    print("-" * 80)
    print(f" {'Category':<20} | {'Samples':<8} | {'Mean Actual':<12} | {'MAE':<8} | {'RMSE':<8} | {'R² Score':<8}")
    print("-" * 80)
    for cat, m in sorted(cat_metrics.items(), key=lambda x: x[1]['R2'], reverse=True):
        print(f" {cat:<20} | {m['sample_count']:<8} | {m['mean_actual_demand']:<12.2f} | {m['MAE']:<8.4f} | {m['RMSE']:<8.4f} | {m['R2']:<8.4f}")
    print("=" * 80)

if __name__ == '__main__':
    run_experiment()
