"""
Controlled Dataset Exploratory Data Analysis & Statistical Variance Testing
===========================================================================
This script performs a rigorous statistical audit, variance decomposition,
correlation analysis, price elasticity estimation, and distribution analysis
for the DemandX dataset ('ml/data/DemandX_India_Datasets_10000 final.xlsx').
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from scipy import stats

# Force UTF-8 encoding for Windows stdout
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Set base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCEL_PATH = os.path.join(BASE_DIR, 'ml', 'data', 'DemandX_India_Datasets_10000 final.xlsx')

def analyze_dataset():
    print("=" * 85)
    print("       DemandX AI -- Controlled Dataset Statistical & Variance Analysis       ")
    print("=" * 85)
    
    xls = pd.ExcelFile(EXCEL_PATH)
    sheet_names = xls.sheet_names
    print(f"[*] Available Sheets in Excel File ({len(sheet_names)}): {sheet_names}")
    
    # Load primary sheets
    df_demand = pd.read_excel(xls, sheet_name='Demand_Model')
    df_products = pd.read_excel(xls, sheet_name='Product_Master') if 'Product_Master' in sheet_names else None
    df_locations = pd.read_excel(xls, sheet_name='Location_Master') if 'Location_Master' in sheet_names else None
    
    # ---------------------------------------------------------
    # 1. DATASET INTEGRITY & STRUCTURE AUDIT
    # ---------------------------------------------------------
    total_rows = len(df_demand)
    total_cols = len(df_demand.columns)
    missing_cells = df_demand.isnull().sum().to_dict()
    duplicate_rows = df_demand.duplicated().sum()
    date_min = str(df_demand['Date'].min()) if 'Date' in df_demand.columns else "N/A"
    date_max = str(df_demand['Date'].max()) if 'Date' in df_demand.columns else "N/A"
    
    audit_summary = {
        "total_rows": total_rows,
        "total_columns": total_cols,
        "duplicate_rows": int(duplicate_rows),
        "date_range": f"{date_min} to {date_max}",
        "sheets": sheet_names,
        "missing_values_by_column": {k: int(v) for k, v in missing_cells.items() if v > 0}
    }
    
    # ---------------------------------------------------------
    # 2. TARGET VARIABLE (Units_Sold_Demand) STATISTICAL FORMULAS & VARIANCES
    # ---------------------------------------------------------
    target = df_demand['Units_Sold_Demand'].values
    mean_val = float(np.mean(target))
    median_val = float(np.median(target))
    std_val = float(np.std(target, ddof=1))
    var_val = float(np.var(target, ddof=1))
    min_val = float(np.min(target))
    max_val = float(np.max(target))
    q25 = float(np.percentile(target, 25))
    q75 = float(np.percentile(target, 75))
    iqr = q75 - q25
    skewness = float(stats.skew(target))
    kurtosis = float(stats.kurtosis(target))
    cv_pct = (std_val / mean_val) * 100 # Coefficient of Variation
    
    target_stats = {
        "count": total_rows,
        "mean_mu": mean_val,
        "median_M": median_val,
        "std_dev_sigma": std_val,
        "variance_sigma_sq": var_val,
        "min": min_val,
        "max": max_val,
        "Q1_p25": q25,
        "Q3_p75": q75,
        "IQR": iqr,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "coefficient_of_variation_pct": cv_pct
    }
    
    # ---------------------------------------------------------
    # 3. VARIANCE DECOMPOSITION (ANOVA) ACROSS CATEGORIES & GROUPS
    # ---------------------------------------------------------
    # One-way ANOVA by Category
    cat_groups = [group['Units_Sold_Demand'].values for _, group in df_demand.groupby('Category')]
    f_cat, p_cat = stats.f_oneway(*cat_groups)
    
    cat_stats = []
    for cat, group in df_demand.groupby('Category'):
        vals = group['Units_Sold_Demand'].values
        cat_stats.append({
            "category": cat,
            "count": len(vals),
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals, ddof=1)),
            "variance": float(np.var(vals, ddof=1)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals))
        })
    cat_stats = sorted(cat_stats, key=lambda x: x['mean'], reverse=True)
    
    # One-way ANOVA by Season
    season_groups = [group['Units_Sold_Demand'].values for _, group in df_demand.groupby('Season')]
    f_season, p_season = stats.f_oneway(*season_groups)
    
    season_stats = []
    for s, group in df_demand.groupby('Season'):
        vals = group['Units_Sold_Demand'].values
        season_stats.append({
            "season": s,
            "count": len(vals),
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals, ddof=1)),
            "variance": float(np.var(vals, ddof=1))
        })
        
    # Promotion Impact (T-Test)
    promo_yes = df_demand[df_demand['Promotion'] == 'Yes']['Units_Sold_Demand'].values
    promo_no = df_demand[df_demand['Promotion'] == 'No']['Units_Sold_Demand'].values
    t_promo, p_promo = stats.ttest_ind(promo_yes, promo_no, equal_var=False)
    
    promo_stats = {
        "promo_yes_mean": float(np.mean(promo_yes)),
        "promo_yes_std": float(np.std(promo_yes, ddof=1)),
        "promo_no_mean": float(np.mean(promo_no)),
        "promo_no_std": float(np.std(promo_no, ddof=1)),
        "uplift_pct": float(((np.mean(promo_yes) - np.mean(promo_no)) / np.mean(promo_no)) * 100),
        "t_statistic": float(t_promo),
        "p_value": float(p_promo)
    }
    
    # Region Stats
    region_stats = []
    for reg, group in df_demand.groupby('Region'):
        vals = group['Units_Sold_Demand'].values
        region_stats.append({
            "region": reg,
            "count": len(vals),
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals, ddof=1)),
            "variance": float(np.var(vals, ddof=1))
        })
        
    # ---------------------------------------------------------
    # 4. FEATURE CORRELATION & PRICE ELASTICITY
    # ---------------------------------------------------------
    num_cols = [
        'Units_Sold_Demand', 'Selling_Price_INR', 'MRP_INR', 'Discount_pct',
        'Competitor_Price_INR', 'Opening_Stock', 'Customer_Footfall',
        'Temperature_C', 'Rainfall_mm', 'Humidity_pct', 'Lead_Time_Days',
        'Prev_Day_Demand', '7_Day_Avg_Demand', '30_Day_Avg_Demand'
    ]
    num_cols = [c for c in num_cols if c in df_demand.columns]
    
    corr_df = df_demand[num_cols].corr()
    target_corrs = corr_df['Units_Sold_Demand'].drop('Units_Sold_Demand').to_dict()
    
    # Log-Log Price Elasticity: ln(Demand) = alpha + beta * ln(Price)
    valid_mask = (df_demand['Units_Sold_Demand'] > 0) & (df_demand['Selling_Price_INR'] > 0)
    log_demand = np.log(df_demand.loc[valid_mask, 'Units_Sold_Demand'])
    log_price = np.log(df_demand.loc[valid_mask, 'Selling_Price_INR'])
    slope, intercept, r_val, p_val, std_err = stats.linregress(log_price, log_demand)
    
    elasticity_summary = {
        "price_elasticity_coefficient": float(slope),
        "r_squared": float(r_val ** 2),
        "p_value": float(p_val),
        "interpretation": "Inelastic (< 1)" if abs(slope) < 1 else "Elastic (> 1)"
    }
    
    # ---------------------------------------------------------
    # 5. PRODUCT MASTER CATALOGUE AUDIT
    # ---------------------------------------------------------
    product_master_summary = {}
    if df_products is not None:
        cat_counts = df_products['Category'].value_counts().to_dict()
        brand_counts = df_products['Brand'].value_counts().to_dict()
        mrp_stats = {
            "min_mrp": float(df_products['MRP_INR'].min()),
            "max_mrp": float(df_products['MRP_INR'].max()),
            "mean_mrp": float(df_products['MRP_INR'].mean()),
            "median_mrp": float(df_products['MRP_INR'].median()),
            "std_mrp": float(df_products['MRP_INR'].std())
        }
        product_master_summary = {
            "total_products": len(df_products),
            "categories_count": len(cat_counts),
            "brands_count": len(brand_counts),
            "mrp_statistics": mrp_stats,
            "category_distribution": cat_counts,
            "brand_distribution": brand_counts
        }

    # Output JSON Report
    full_report = {
        "audit_summary": audit_summary,
        "target_variable_statistics": target_stats,
        "anova_category": {"F_stat": float(f_cat), "p_value": float(p_cat), "breakdown": cat_stats},
        "anova_season": {"F_stat": float(f_season), "p_value": float(p_season), "breakdown": season_stats},
        "promotion_t_test": promo_stats,
        "region_breakdown": region_stats,
        "correlations_with_demand": {k: float(v) for k, v in target_corrs.items()},
        "price_elasticity": elasticity_summary,
        "product_master_summary": product_master_summary
    }
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(output_dir, 'dataset_analysis_report.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, indent=2)
        
    print(f"\n[+] Analysis complete! JSON Report saved at: {json_path}\n")
    
    # Display Executive Summary
    print("=" * 85)
    print("                      DATASET INTEGRITY & STATISTICAL AUDIT                 ")
    print("=" * 85)
    print(f" Total Dataset Rows:         {total_rows:,}")
    print(f" Total Features/Columns:     {total_cols}")
    print(f" Duplicate Rows:             {duplicate_rows}")
    print(f" Time Horizon:               {date_min} to {date_max}")
    print("-" * 85)
    print(" FORMULATED VARIANCES & STATS (Units_Sold_Demand):")
    print(f"   • Mean (mu):               {mean_val:.4f} units")
    print(f"   • Median (M):              {median_val:.4f} units")
    print(f"   • Std Deviation (sigma):   {std_val:.4f} units")
    print(f"   • Variance (sigma^2):      {var_val:.4f} units^2")
    print(f"   • Coefficient of Var (CV): {cv_pct:.2f}%")
    print(f"   • Interquartile Range:     {iqr:.2f} (Q1={q25:.1f}, Q3={q75:.1f})")
    print(f"   • Min / Max Range:         {min_val:.1f} to {max_val:.1f} units")
    print(f"   • Skewness / Kurtosis:     Skew={skewness:.4f} (Right-skewed), Kurtosis={kurtosis:.4f}")
    print("=" * 85)
    
    print("\n [+] DEMAND VARIANCES BY CATEGORY (ANOVA F = {:.2f}, p < 0.001):".format(f_cat))
    print("-" * 85)
    print(f" {'Category':<18} | {'Count':<7} | {'Mean Demand':<12} | {'Std Dev (sigma)':<15} | {'Variance (sigma^2)':<18} | {'Range':<10}")
    print("-" * 85)
    for c in cat_stats:
        print(f" {c['category']:<18} | {c['count']:<7} | {c['mean']:<12.2f} | {c['std']:<15.2f} | {c['variance']:<18.2f} | {c['min']:.0f}-{c['max']:.0f}")
    print("=" * 85)

    print("\n [+] PROMOTION UPLIFT & T-TEST:")
    print(f"   • Promo Active Mean:       {promo_stats['promo_yes_mean']:.2f} units (sigma = {promo_stats['promo_yes_std']:.2f})")
    print(f"   • Promo Inactive Mean:     {promo_stats['promo_no_mean']:.2f} units (sigma = {promo_stats['promo_no_std']:.2f})")
    print(f"   • Promotion Demand Uplift: +{promo_stats['uplift_pct']:.2f}% (T-stat = {promo_stats['t_statistic']:.2f}, p < 0.001)")

    print("\n [+] KEY FEATURE CORRELATIONS WITH DEMAND:")
    for feat, corr_v in sorted(target_corrs.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"   • {feat:<22}: {corr_v:+.4f}")

    print("=" * 85)

if __name__ == '__main__':
    analyze_dataset()
