"""
Stock Price Prediction - ARIMA Model
This script builds an ARIMA time series model for stock price prediction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import math
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Create plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)
os.makedirs('models', exist_ok=True)

print("Loading preprocessed data...")
try:
    # Load the preprocessed data
    data = pd.read_csv('data/preprocessed_data.csv', index_col=0, parse_dates=True)
    
    # Check for stationarity
    def check_stationarity(timeseries):
        # Perform Dickey-Fuller test
        result = adfuller(timeseries)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))
        
        # If p-value is less than 0.05, data is stationary
        if result[1] <= 0.05:
            print("Data is stationary")
            return True
        else:
            print("Data is not stationary")
            return False
    
    print("\nChecking stationarity of Close prices...")
    is_stationary = check_stationarity(data['Close'])
    
    # If not stationary, difference the data
    if not is_stationary:
        print("Differencing data to make it stationary...")
        data['Close_diff'] = data['Close'].diff().dropna()
        check_stationarity(data['Close_diff'])
        # Plot differenced data
        plt.figure(figsize=(10, 6))
        plt.plot(data['Close_diff'])
        plt.title('Differenced Close Prices')
        plt.xlabel('Date')
        plt.ylabel('Price Difference')
        plt.grid(True)
        plt.savefig('plots/differenced_close.png')
        plt.close()
    else:
        data['Close_diff'] = data['Close']
        
    # Split data for ARIMA
    train_size = int(len(data) * 0.8)
    train_data = data['Close'][:train_size]
    test_data = data['Close'][train_size:]
    
    print(f"\nTraining data size: {len(train_data)}")
    print(f"Testing data size: {len(test_data)}")
    
    # ARIMA parameter selection
    # For simplicity, we'll use fixed parameters, but in practice
    # you would use techniques like AIC or grid search to find optimal parameters
    p, d, q = 5, 1, 0  # Example parameters
    
    print(f"\nFitting ARIMA({p},{d},{q}) model...")
    model = ARIMA(train_data, order=(p, d, q))
    model_fit = model.fit()
    print(model_fit.summary())
    
    # Make predictions
    print("\nMaking predictions...")
    predictions = model_fit.forecast(steps=len(test_data))
    
    # Evaluate model
    rmse = math.sqrt(mean_squared_error(test_data, predictions))
    mae = mean_absolute_error(test_data, predictions)
    mape = np.mean(np.abs((test_data - predictions) / test_data)) * 100
    
    print(f"\nModel Evaluation Metrics:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"MAPE: {mape:.2f}%")
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(test_data.index, test_data, label='Actual')
    plt.plot(test_data.index, predictions, label='Predicted', color='red')
    plt.title('ARIMA: Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/arima_prediction.png')
    plt.close()
    
    # Save predictions for later comparison
    predictions_df = pd.DataFrame({
        'Actual': test_data.values,
        'Predicted': predictions
    }, index=test_data.index)
    predictions_df.to_csv('data/arima_predictions.csv')
    
    # Save the model
    with open('models/arima_model.pkl', 'wb') as f:
        pickle.dump(model_fit, f)
    
    # Make future predictions (next 30 days)
    print("\nMaking future predictions (next 30 days)...")
    future_days = 30
    future_predictions = model_fit.forecast(steps=future_days)
    future_dates = pd.date_range(start=data.index[-1], periods=future_days+1)[1:]
    
    future_df = pd.DataFrame({
        'Predicted_Price': future_predictions
    }, index=future_dates)
    
    future_df.to_csv('data/arima_future_predictions.csv')
    
    # Plot future predictions
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'][-60:].index, data['Close'][-60:], label='Historical Data')
    plt.plot(future_dates, future_predictions, label='ARIMA Forecast', color='red', linestyle='--')
    plt.title('ARIMA: Future Stock Price Forecast (Next 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/arima_future_forecast.png')
    plt.close()
    
    print("\nARIMA model completed successfully!")
    print("Results saved in 'plots' and 'models' directories")
    
except Exception as e:
    print(f"An error occurred: {e}")
