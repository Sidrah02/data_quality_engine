import streamlit as st
import pandas as pd
import quality_checks as qc
import cleaning

st.set_page_config(page_title="Data Quality Engine", page_icon="🧹", layout="wide")

st.title("Data Quality Engine")
st.markdown("### A simple rule-based data cleaning and validation tool.")

# File Uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load Data
        df = pd.read_csv(uploaded_file)
        
        # --- Section 1: Dataset Overview ---
        st.divider()
        st.subheader("1. Dataset Overview")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
            
        st.write("First 20 Rows:")
        st.dataframe(df.head(20))
        
        st.write("Column Information:")
        missing_df = qc.check_missing_values(df)
        if not missing_df.empty:
            st.warning(f"Found missing values in {len(missing_df)} columns.")
        else:
            st.success("No missing values found.")
            
        # --- Section 2: Data Quality Checks ---
        st.divider()
        st.subheader("2. Data Quality Checks")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Missing Values", "Duplicates", "Outliers", "Inconsistent Formats", "Basic Validation"
        ])
        
        with tab1:
            st.markdown("#### A) Missing Values")
            if not missing_df.empty:
                st.dataframe(missing_df)
            else:
                st.info("No missing values detected.")
                
        with tab2:
            st.markdown("#### B) Duplicate Rows")
            dup_count, dup_rows = qc.check_duplicates(df)
            st.metric("Duplicate Rows Count", dup_count)
            if dup_count > 0:
                st.write("Preview of Duplicates:")
                st.dataframe(dup_rows.head(10))
                
        with tab3:
            st.markdown("#### C) Outliers (Numeric - IQR Method)")
            outliers = qc.check_outliers(df)
            if outliers:
                for col, data in outliers.items():
                    with st.expander(f"Column: {col} ({data['count']} outliers)"):
                        st.dataframe(data['sample'])
            else:
                st.info("No outliers detected in numeric columns.")

        with tab4:
            st.markdown("#### D) Inconsistent Formats")
            mixed_types = qc.check_mixed_data_types(df)
            if mixed_types:
                for col, msg in mixed_types.items():
                    st.write(f"- **{col}**: {msg}")
            else:
                st.info("No mixed data types detected.")
                
        with tab5:
            st.markdown("#### E) Basic Validation")
            validation_issues = qc.check_basic_validation(df)
            
            has_issues = False
            if validation_issues['empty_strings']:
                st.write("**Empty/Whitespace Only Strings:**")
                for col, count in validation_issues['empty_strings'].items():
                    st.write(f"- {col}: {count} rows")
                has_issues = True
                
            if validation_issues['negative_values']:
                st.write("**Negative Values in Numeric Columns:**")
                for col, count in validation_issues['negative_values'].items():
                    st.write(f"- {col}: {count} rows")
                has_issues = True
                
            if validation_issues['invalid_emails']:
                st.write("**Invalid Emails:**")
                for col, count in validation_issues['invalid_emails'].items():
                    st.write(f"- {col}: {count} invalid emails")
                has_issues = True
                
            if not has_issues:
                st.info("No basic validation issues found.")

        # --- Section 3: Cleaning Module ---
        st.divider()
        st.subheader("3. Data Cleaning Module")
        
        col_clean1, col_clean2 = st.columns(2)
        
        with col_clean1:
            clean_opts = {
                'drop_duplicates': st.checkbox(f"Drop Duplicate Rows ({dup_count} found)"),
                'fill_numeric': st.checkbox("Fill Missing Numeric Values (Median)"),
                'fill_categorical': st.checkbox("Fill Missing Categorical Values (Mode)"),
            }
        with col_clean2:
            clean_opts.update({
                'trim_whitespace': st.checkbox("Trim Whitespace from Strings"),
                'standardize_cols': st.checkbox("Standardize Column Names (snake_case)"),
            })

        if st.button("Apply Cleaning", type="primary"):
            cleaned_df = cleaning.clean_data(df, clean_opts)
            
            st.success("Cleaning operations applied!")
            st.write("Cleaned Dataset Preview:")
            st.dataframe(cleaned_df.head(20))
            
            st.markdown(f"**Cleaned Data Shape:** {cleaned_df.shape[0]} rows, {cleaned_df.shape[1]} columns")
            
            # CSV Download
            csv = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Cleaned CSV",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a CSV file to begin.")
