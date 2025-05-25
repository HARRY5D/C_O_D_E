# Stock Price Prediction Project

This project implements time series forecasting models to predict stock prices using historical data from Yahoo Finance. The project compares the performance of ARIMA (statistical model) and LSTM (deep learning) approaches.

## Features

- Data collection from Yahoo Finance API
- Data preprocessing and feature engineering
- Technical indicators (Moving Averages, RSI, MACD, Bollinger Bands)
- ARIMA time series model implementation
- LSTM deep learning model implementation
- Model comparison and evaluation
- Future price prediction
- Ensemble prediction

## Project Structure

```
StockPrediction/
│
├── data/                  # Directory for stored data
│
├── models/                # Directory for trained models
│
├── plots/                 # Directory for generated plots
│
├── results/               # Directory for prediction results
│
├── data_preprocessing.py  # Script for data collection and preprocessing
├── arima_model.py         # ARIMA model implementation
├── lstm_model.py          # LSTM model implementation
├── model_comparison.py    # Model comparison script
├── predict.py             # Prediction API script
├── run_pipeline.py        # Main runner script
└── README.md              # This file
```

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- scikit-learn
- tensorflow
- yfinance
- statsmodels

## Usage

### Quick Start

1. Run the entire pipeline with default settings (AAPL stock, 30-day prediction):

```
python run_pipeline.py
```

2. Specify a different stock and prediction period:

```
python run_pipeline.py --ticker MSFT --days 60
```

### Step-by-Step Execution

1. Data preprocessing:

```
python data_preprocessing.py
```

2. Train and evaluate ARIMA model:

```
python arima_model.py
```

3. Train and evaluate LSTM model:

```
python lstm_model.py
```

4. Compare model performance:

```
python model_comparison.py
```

5. Make predictions:

```
python predict.py
```

## Results

After running the pipeline:

1. Check the `plots/` directory for visualizations:
   - Stock price history
   - Technical indicators
   - Model predictions vs actual prices
   - Future forecasts

2. Check the `results/` directory for:
   - Model comparison metrics
   - Future price predictions

## Model Performance

The project automatically compares ARIMA and LSTM models using:
- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)
- Mean Absolute Percentage Error (MAPE)

## Limitations

- Past performance does not guarantee future results
- Market sentiment, news events, and macroeconomic factors are not considered
- The models work better for stable stocks and less reliably for volatile ones
- These predictions should be used for educational purposes only and not for financial decisions

## Future Improvements

- Include sentiment analysis from news and social media
- Add more technical indicators
- Implement hyperparameter tuning
- Add more advanced models (Prophet, XGBoost, etc.)
- Create a web interface for interactive predictions
