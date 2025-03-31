# Gold Price Prediction Project

## Overview

This project aims to predict gold price movements using a diverse set of features and ultimately implement a trading strategy that can be backtested. The model will focus on predicting the difference between the opening price and the highest or lowest price of the day (whichever is larger). A Long Short-Term Memory (LSTM) neural network will be used to capture temporal dependencies in the data.

## Project Structure

  - **`src/data/`**: Contains scripts for fetching data (e.g., `bls_api.py`, `news_sentiment.py`) and consolidating it into a single dataset.
  - **`data/raw/`**: Holds raw CSV files such as gold, oil, and DXY prices.
  - **`data/external/`**: Contains external economic data (e.g., FEDFUNDS, GS10, M2REAL).
  - **`data/processed/`**: Stores processed or partially cleaned data (e.g., `bls_data.csv`, `consolidated.csv`).
  - **`notebooks/`**: Jupyter notebooks for data exploration and feature selection and engineering, data modelling and strategy implementation and backtesting.

## Current Progress

1. **Data Collection**
  
  - **Gold, Oil, and DXY Prices**: Fetched daily data using `yfinance`.
  
  - **Economic Indices**: Downloaded monthly data from the Bureau of Labor Statistics (BLS) and the Federal Reserve Economic Data (FRED)
  
    - BLS
      - Consumer Price Index (CPI)
      - The unemployment rate for the civilian labor force (NFP)
      - Producer Price Index (PPI)
      
    - FRED
      - The effective Federal Funds Rate (FEDFUNDS)
      - The 10-Year Treasury Constant Maturity Rate (GS10)
      - Real M2 Money Stock—a measure of the money supply adjusted for inflation (M2REAL)

  - **Consolidation**:  
    - Economic indices, which are monthly, are repeated daily within each month to align with the daily price data.  
    - A consolidated CSV file (`consolidated_data.csv`) has been created by merging all data sources on a daily timeline.

2. **Data Wrangling**
  
  - Created a Jupyter notebook (join_data.ipynb):
  
    - Loads all CSV files (gold, oil, DXY, FRED and BLS data).
    - Converts relevant columns to `datetime`.
    - Uses `merge_asof` to combine daily market data with monthly economic indices.
    - Pivots BLS data so each `seriesID` becomes its own column.
    - Produced a final consolidated dataset ready for modeling.

3. **Feature Selection & Engineering**
  
  - **Analysis:**  
    - Performed correlation analysis, mutual information, and Recursive Feature Elimination (RFE) to determine the most informative features.

  - **Created technical indicators:**  
    - Technical indicators were created from the available data (EMA of 21 and 200 periods, RSI of 14 periods, etc) for capturing market trends.

  - **Selected Feature Sets:**  
    - Saved three different datasets (RFE, MI-based, and RF-based) for later comparison during the modeling phase.

4. **Modeling**
  
  - **Initial LSTM Implementation:**  
    - Built an LSTM model to predict the target.
    - Created sequences with a fixed window.
    - Encountered flat predictions (near zero) for all feature sets—indicating that the model is currently not capturing the variability in the target.

### Current Limitations
  
  - **Flat Predictions:**  
    - The current LSTM model is producing constant predictions across all feature sets.
    
  - **Seasonality & Train-Test Split:**  
    - The training and test sets have not yet been updated to capture seasonal patterns (i.e., using the first 6 years for training and the last 2 years for testing).

## Next Steps

1. **Update Train-Test Split for Seasonality:**  
  - Revise the data preparation phase to split the dataset into 6 years for training and 2 years for testing. This will help capture seasonal trends.
  
2. **Model Refinement:**  
  - Experiment with scaling or transforming the target variable.
  - Adjust the LSTM architecture (e.g., increase layers/units, tune hyperparameters) to improve learning.
  - Consider additional or alternative feature engineering strategies.
  
3. **Feature Set Comparison:**  
  - Evaluate performance across the three saved datasets (RFE, MI-based, RF-based) to determine which feature set yields the best predictive performance.
  
4. **Validation & Backtesting:**  
  - Once the model begins to capture non-flat predictions, integrate backtesting for the trading strategy targeting 70% of the predicted move.

## Requirements

- Python 3.11+
- Key libraries: `pandas`, `numpy`, `requests`, `yfinance`, `matplotlib`, etc.
- (Future) `tensorflow` or `pytorch` for LSTM modeling and `backtrader`