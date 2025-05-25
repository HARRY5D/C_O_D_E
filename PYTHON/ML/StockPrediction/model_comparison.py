"""
Stock Price Prediction - Model Comparison
This script compares the performance of ARIMA and LSTM models
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Create plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)
os.makedirs('results', exist_ok=True)

print("Loading prediction results...")

try:
    # Load predictions
    arima_predictions = pd.read_csv('data/arima_predictions.csv', index_col=0, parse_dates=True)
    lstm_predictions = pd.read_csv('data/lstm_predictions.csv', index_col=0, parse_dates=True)
    
    # Load future predictions
    arima_future = pd.read_csv('data/arima_future_predictions.csv', index_col=0, parse_dates=True)
    lstm_future = pd.read_csv('data/lstm_future_predictions.csv', index_col=0, parse_dates=True)
    
    # Make sure the ARIMA predictions align with the LSTM predictions
    # First, find common dates
    common_dates = arima_predictions.index.intersection(lstm_predictions.index)
    
    if len(common_dates) == 0:
        print("No common dates found between ARIMA and LSTM predictions.")
        # Use last N predictions where N is the minimum length
        min_length = min(len(arima_predictions), len(lstm_predictions))
        arima_subset = arima_predictions.iloc[-min_length:]
        lstm_subset = lstm_predictions.iloc[-min_length:]
    else:
        arima_subset = arima_predictions.loc[common_dates]
        lstm_subset = lstm_predictions.loc[common_dates]
    
    # Calculate metrics for comparison
    arima_rmse = math.sqrt(mean_squared_error(arima_subset['Actual'], arima_subset['Predicted']))
    arima_mae = mean_absolute_error(arima_subset['Actual'], arima_subset['Predicted'])
    arima_mape = np.mean(np.abs((arima_subset['Actual'] - arima_subset['Predicted']) / arima_subset['Actual'])) * 100
    
    lstm_rmse = math.sqrt(mean_squared_error(lstm_subset['Actual'], lstm_subset['Predicted']))
    lstm_mae = mean_absolute_error(lstm_subset['Actual'], lstm_subset['Predicted'])
    lstm_mape = np.mean(np.abs((lstm_subset['Actual'] - lstm_subset['Predicted']) / lstm_subset['Actual'])) * 100
    
    # Print comparison
    print("\nModel Performance Comparison:")
    print(f"{'Metric':<10} {'ARIMA':>10} {'LSTM':>10}")
    print("-" * 30)
    print(f"{'RMSE':<10} {arima_rmse:>10.2f} {lstm_rmse:>10.2f}")
    print(f"{'MAE':<10} {arima_mae:>10.2f} {lstm_mae:>10.2f}")
    print(f"{'MAPE':<10} {arima_mape:>10.2f}% {lstm_mape:>10.2f}%")
    
    # Determine the better model
    if lstm_rmse < arima_rmse:
        print("\nLSTM model performs better based on RMSE.")
        better_model = "LSTM"
    else:
        print("\nARIMA model performs better based on RMSE.")
        better_model = "ARIMA"
        
    # Create comparison plot
    plt.figure(figsize=(12, 6))
    plt.plot(arima_subset.index, arima_subset['Actual'], label='Actual', color='blue')
    plt.plot(arima_subset.index, arima_subset['Predicted'], label='ARIMA Predictions', color='red', linestyle='--')
    plt.plot(lstm_subset.index, lstm_subset['Predicted'], label='LSTM Predictions', color='green', linestyle=':')
    plt.title('Model Comparison: ARIMA vs LSTM')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/model_comparison.png')
    plt.close()
    
    # Create future predictions comparison plot
    # Combine future predictions
    future_predictions = pd.DataFrame({
        'ARIMA': arima_future['Predicted_Price'],
        'LSTM': lstm_future['Predicted_Price']
    })
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(future_predictions.index, future_predictions['ARIMA'], 
             label='ARIMA Forecast', color='red', linestyle='--')
    plt.plot(future_predictions.index, future_predictions['LSTM'], 
             label='LSTM Forecast', color='green', linestyle=':')
    plt.title('Future Price Forecast Comparison (Next 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/future_forecast_comparison.png')
    plt.close()
    
    # Save comparison results
    comparison_results = {
        'ARIMA_RMSE': arima_rmse,
        'ARIMA_MAE': arima_mae,
        'ARIMA_MAPE': arima_mape,
        'LSTM_RMSE': lstm_rmse,
        'LSTM_MAE': lstm_mae,
        'LSTM_MAPE': lstm_mape,
        'Better_Model': better_model
    }
    
    comparison_df = pd.DataFrame([comparison_results])
    comparison_df.to_csv('results/model_comparison_results.csv', index=False)
    
    # Save future predictions
    future_predictions.to_csv('results/future_predictions_combined.csv')
    
    print("\nModel comparison completed successfully!")
    print("Results saved in 'plots' and 'results' directories")
    
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Make sure both ARIMA and LSTM models have been run first.")
except Exception as e:
    print(f"An error occurred: {e}")
