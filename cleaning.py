import pandas as pd
import numpy as np

def clean_data(df, options):
    """
    Applies cleaning operations based on the provided options dictionary.
    options = {
        'drop_duplicates': bool,
        'fill_numeric': bool, # fill with median
        'fill_categorical': bool, # fill with mode
        'trim_whitespace': bool,
        'standardize_cols': bool
    }
    """
    df_cleaned = df.copy()
    
    # 1. Drop Duplicates
    if options.get('drop_duplicates'):
        df_cleaned = df_cleaned.drop_duplicates()
        
    # 2. Fill Missing Numeric Values (Median)
    if options.get('fill_numeric'):
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_cleaned[col].isnull().any():
                median_val = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_val)
                
    # 3. Fill Missing Categorical Values (Mode)
    if options.get('fill_categorical'):
        cat_cols = df_cleaned.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            if df_cleaned[col].isnull().any():
                # Mode can be empty if all are NaN, so check
                mode_series = df_cleaned[col].mode()
                if not mode_series.empty:
                    df_cleaned[col] = df_cleaned[col].fillna(mode_series[0])
                    
    # 4. Trim Whitespace from String Columns
    if options.get('trim_whitespace'):
        str_cols = df_cleaned.select_dtypes(include=['object']).columns
        for col in str_cols:
            df_cleaned[col] = df_cleaned[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            
    # 5. Standardize Column Names
    if options.get('standardize_cols'):
        df_cleaned.columns = df_cleaned.columns.str.lower().str.replace(' ', '_').str.replace(r'[^\w\s]', '', regex=True)
        
    return df_cleaned
