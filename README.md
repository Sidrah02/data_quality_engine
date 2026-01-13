# Data Quality Engine

A simple, rule-based data cleaning and validation tool built with Python and Streamlit.

## Features
- **Upload CSV**: Analyze any CSV dataset.
- **Data Overview**: View rows, columns, and missing value statistics.
- **Quality Checks**:
    - Missing Values Detection
    - Duplicate Row Detection
    - Outlier Detection (IQR Method)
    - Inconsistent Format Detection
    - Basic Validation (Empty strings, negative values, invalid emails)
- **Data Cleaning**:
    - Drop duplicates
    - Impute missing values (Median/Mode)
    - Trim whitespace
    - Standardize column names
- **Export**: Download results as a clean CSV file.

## Installation

1. Clone or download this project.
2. Navigate to the project folder:
   ```bash
   cd data-quality-engine
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser at `http://localhost:8501`.

## Deployment (Streamlit Community Cloud)
1. Push this code to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and select the repository.
4. Set the "Main file path" to `app.py`.
5. Click **Deploy**.
