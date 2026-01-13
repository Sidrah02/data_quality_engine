import pandas as pd
import numpy as np
import re

def check_missing_values(df):
    """Checks for missing values in the dataframe."""
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
    return missing_df[missing_df['Missing Count'] > 0]

def check_duplicates(df):
    """Checks for duplicate rows."""
    dup_count = df.duplicated().sum()
    dup_rows = df[df.duplicated()]
    return dup_count, dup_rows

def check_outliers(df):
    """Checks for outliers in numeric columns using IQR method."""
    outlier_report = {}
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        
        if not outliers.empty:
            outlier_report[col] = {
                'count': len(outliers),
                'sample': outliers.head(5)
            }
            
    return outlier_report

def check_mixed_data_types(df):
    """Checks for columns with mixed data types."""
    mixed_types = {}
    for col in df.columns:
        # Check if column has mixed types (ignoring NaNs)
        unique_types = df[col].dropna().apply(type).nunique()
        if unique_types > 1:
            mixed_types[col] = "Mixed types detected"
    return mixed_types

def check_basic_validation(df):
    """Performs basic validation checks."""
    issues = {
        'empty_strings': {},
        'negative_values': {},
        'invalid_emails': {}
    }
    
    # Check for empty or whitespace-only strings
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        empty_mask = df[col].astype(str).str.strip() == ''
        empty_count = empty_mask.sum()
        if empty_count > 0:
            issues['empty_strings'][col] = empty_count
            
    # Check for negative values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            issues['negative_values'][col] = neg_count
            
    # Check for invalid emails
    email_cols = [col for col in df.columns if 'email' in col.lower()]
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    for col in email_cols:
        # Simple check: Convert to string, match regex. NaNs are ignored.
        non_matching = df[col].dropna().apply(lambda x: not bool(re.match(email_regex, str(x))))
        invalid_count = non_matching.sum()
        if invalid_count > 0:
            issues['invalid_emails'][col] = invalid_count
            
    return issues
