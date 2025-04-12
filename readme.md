# Gold Price Prediction Project

## Overview

This project aims to predict gold price movements using a diverse set of features and ultimately implement a trading strategy that can be backtested. The model focuses on predicting the difference between the opening price and the highest or lowest price of the day (whichever is larger). A Long Short-Term Memory (LSTM) neural network is used to capture temporal dependencies in the data.

## Project Structure

- **`src/data/`**: Contains subfolders and files of data sources and outputs
- **`data/external/`**: Contains external economic data manually downloaded from FRED (e.g., FEDFUNDS, GS10, M2REAL).
- **`data/processed/`**: Stores processed or partially cleaned data (e.g., `bls_data.csv`, `consolidated_data.csv`).
- **`notebooks/`**: Jupyter notebooks for data exploration, feature selection/engineering, modeling, and strategy/backtesting.
- **`src/`**: Contains scripts for fetching data (`bls_api.py`, `news_sentiment.py`)

## Data Collection

- **Gold, Oil, and DXY Prices**: Fetched daily data using `yfinance`.
- **Economic Indices**: Downloaded monthly data from the Bureau of Labor Statistics (BLS) using its API (CPI, Unemployment Rate, PPI, NFP. see `bls_api.py`).
- **News Sentiment**: Tried connecting to AlphaVantage's API but the news sentiment feature is novel and is only providing 2 days of data (`news_sentiment.py` script).  
- **Consolidation**:  
  - Economic indices, which are monthly, are repeated daily within each month to align with the daily price data.  
  - A consolidated CSV file (`consolidated.csv`) has been created by merging all data sources on a daily timeline.

## How to Go Through the Project

1. **Data Preparation**  
   - Begin by joining the data in the `notebooks/` folder. Use `00_join_data.ipynb` and `01_data_preprocessing.ipynb` to see how raw data is combined and cleaned.

2. **Feature Engineering & Selection**  
   - Move on to `02_feature_selection.ipynb` to review how technical indicators (EMA, RSI, etc.) were created and to see the results of correlation analysis, mutual information, Recursive Feature Elimination (RFE) and Feature Importance using Random Forest (RF).  
   - Three separate datasets (RFE, MI-based, RF-based) have been saved under `data/processed/` for later comparison.

3. **Modeling**  
   - Check out `03_modelling.ipynb` to observe the LSTM model implementation.  
   - The model uses a 63 fixed window sequence to capture market movement and patterns per quarter, and ultimately predict next-day movements

4. **Strategy & Backtesting**  
   - Review `04_backtesting.ipynb` to explore various attempts to implement a trading strategy using the model's predictions.  
   - This notebook includes integration with the backtesting library.

## Model Performance Results

- **Initial LSTM Findings:**  
  - The LSTM model initially predicted near-zero values across different feature sets, indicating that the model is converging to the mean target instead of capturing meaningful variability.
  - Preliminary metrics (e.g., RMSE and MAE) reflect that the model’s current performance does not fully capture next-day price dynamics.

## Strategy Results and Takeaways

- **Strategy Backtesting Integration:**  
  - We implemented a backtesting module using a dedicated library, allowing us to simulate the trading strategy on our predicted data.
  - The strategy was designed to take trades based on the model’s predictions (targeting 70% of the predicted move with predefined stop loss and take profit levels).

- **Key Metrics Observed:**  
  - Relevant metrics such as the number of trades, win rate, market exposure, maximum drawdown, etc., were tracked.
  
- **Challenges Encountered:**  
  - Although the raw backtest results appear positive, the execution and entry timing of trades were not implemented as expected.
  - Different methods, calculations, and entry types were tested, but none of them returned the results anticipated by the strategy design.  
  - This indicates that further refinements in terms of parameters and strategy logic are needed before the approach can be fully validated.

## Next Steps

1. **Implement Time Series Cross-Validation:**  
   - Explore using `TimeSeriesSplit` to perform cross-validation across multiple temporal folds. This will help to robustly evaluate model performance and better capture temporal variability in the data.

2. **Refine the Model:**  
   - Adjust the LSTM architecture (e.g., adding more layers/units, tuning hyperparameters) to improve learning.
   - Explore additional feature engineering strategies.

3. **Feature Set Comparison:**  
   - Evaluate the performance across different feature sets (RFE, MI-based, RF-based) to determine which one yields the best results.

4. **Backtesting Validation:**  
   - Refine the strategy implementation to ensure trades are executed at the intended times (e.g., at the next candle’s open).

## Requirements

- Python 3.11+
- Key libraries: `pandas`, `numpy`, `requests`, `yfinance`, `matplotlib`, `tensorflow`, `backtesting`, `scikit-learn`