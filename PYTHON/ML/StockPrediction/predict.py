"""
Stock Price Prediction - Prediction API
This script provides functions to predict stock prices using trained models
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import yfinance as yf
import tensorflow as tf
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMAResults

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

def load_models():
    """Load trained ARIMA and LSTM models"""
    try:
        # Load ARIMA model
        with open('models/arima_model.pkl', 'rb') as f:
            arima_model = pickle.load(f)
            
        # Load LSTM model
        lstm_model = tf.keras.models.load_model('models/lstm_model.h5')
        
        # Load scaler
        with open('data/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
            
        return arima_model, lstm_model, scaler
    except FileNotFoundError:
        print("Model files not found. Please train models first.")
        return None, None, None

def get_latest_data(ticker, days=365):
    """Get the latest stock data for the specified ticker"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def preprocess_data(data):
    """Preprocess data for LSTM model"""
    # Add technical indicators
    def add_technical_indicators(df):
        # Moving averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        # Bollinger Bands
        df['20d_std'] = df['Close'].rolling(window=20).std()
        df['upper_band'] = df['MA20'] + (df['20d_std'] * 2)
        df['lower_band'] = df['MA20'] - (df['20d_std'] * 2)
        
        # RSI (14-day)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        return df
    
    data = add_technical_indicators(data)
    data.dropna(inplace=True)
    
    return data

def predict_stock_price(ticker_symbol, days=30):
    """
    Predict stock prices for the specified ticker for the next N days
    
    Parameters:
    ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL')
    days (int): Number of days to predict
    
    Returns:
    DataFrame: Predictions from both models with dates
    """
    print(f"Predicting {days} days ahead for {ticker_symbol}...")
    
    # Load models
    arima_model, lstm_model, scaler = load_models()
    if arima_model is None or lstm_model is None:
        return None
    
    # Get latest data
    latest_data = get_latest_data(ticker_symbol)
    
    # Preprocess data
    processed_data = preprocess_data(latest_data)
    
    # Features for LSTM
    features = ['Close', 'Volume', 'MA20', 'MA50', 'RSI', 'MACD', 'upper_band', 'lower_band']
    
    # ARIMA future prediction
    arima_future = arima_model.forecast(steps=days)
    
    # Prepare data for LSTM
    sequence_length = 60  # This should match what was used during training
    
    # Scale the data
    scaled_data = scaler.transform(processed_data[features])
    
    # Get the last sequence
    last_sequence = scaled_data[-sequence_length:].reshape(1, sequence_length, len(features))
    
    # Predict with LSTM
    lstm_future = []
    current_sequence = last_sequence.copy()
    
    for _ in range(days):
        next_pred = lstm_model.predict(current_sequence, verbose=0)
        lstm_future.append(next_pred[0, 0])
        
        # Update sequence by dropping the first element and adding the new prediction
        new_data_point = np.zeros((1, len(features)))
        new_data_point[0, 0] = next_pred[0, 0]  # Set the predicted close price
        
        current_sequence = np.concatenate([
            current_sequence[:, 1:, :],  # Remove first time step
            new_data_point.reshape(1, 1, len(features))  # Add new prediction
        ], axis=1)
    
    # Scale back the LSTM predictions
    lstm_future_array = np.array(lstm_future).reshape(-1, 1)
    lstm_future_full = np.zeros((len(lstm_future), len(features)))
    lstm_future_full[:, 0] = lstm_future_array.flatten()
    lstm_future_original = scaler.inverse_transform(lstm_future_full)[:, 0]
    
    # Create future dates
    future_dates = pd.date_range(start=processed_data.index[-1], periods=days+1)[1:]
    
    # Create result DataFrame
    results = pd.DataFrame({
        'Date': future_dates,
        'ARIMA_Prediction': arima_future,
        'LSTM_Prediction': lstm_future_original
    })
    
    # Also include a weighted ensemble prediction (You can adjust the weights)
    # Based on your model comparison, give more weight to the better performing model
    with open('results/model_comparison_results.csv', 'r') as f:
        comparison_results = pd.read_csv(f)
        
    if comparison_results['Better_Model'].values[0] == 'LSTM':
        lstm_weight = 0.7
        arima_weight = 0.3
    else:
        lstm_weight = 0.3
        arima_weight = 0.7
    
    results['Ensemble_Prediction'] = (
        results['ARIMA_Prediction'] * arima_weight + 
        results['LSTM_Prediction'] * lstm_weight
    )
    
    # Save the predictions
    results.to_csv(f'results/{ticker_symbol}_predictions.csv', index=False)
    
    # Create a plot
    plt.figure(figsize=(12, 6))
    
    # Plot historical data
    plt.plot(processed_data.index[-30:], processed_data['Close'][-30:], label='Historical Data')
    
    # Plot predictions
    plt.plot(results['Date'], results['ARIMA_Prediction'], label='ARIMA', linestyle='--')
    plt.plot(results['Date'], results['LSTM_Prediction'], label='LSTM', linestyle=':')
    plt.plot(results['Date'], results['Ensemble_Prediction'], label='Ensemble', linestyle='-.')
    
    plt.title(f'{ticker_symbol} Stock Price Prediction (Next {days} Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'results/{ticker_symbol}_prediction_plot.png')
    plt.close()
    
    return results

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"  # Default ticker
    days = 30  # Default prediction days
    
    # You can modify this to accept command line arguments
    # import argparse
    # parser = argparse.ArgumentParser(description='Predict stock prices')
    # parser.add_argument('--ticker', default='AAPL', help='Stock ticker symbol')
    # parser.add_argument('--days', type=int, default=30, help='Number of days to predict')
    # args = parser.parse_args()
    # ticker = args.ticker
    # days = args.days
    
    predictions = predict_stock_price(ticker, days)
    
    if predictions is not None:
        print(f"\nPredictions for {ticker} (next {days} days):")
        print(predictions.head())
        print(f"\nFull predictions saved to results/{ticker}_predictions.csv")
        print(f"Prediction plot saved to results/{ticker}_prediction_plot.png")
