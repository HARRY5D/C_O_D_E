"""
Stock Price Prediction - Data Collection and Preprocessing
This script downloads historical stock data and prepares it for model training
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import os
import pickle

# Create plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Configuration
TICKER = "AAPL"
START_DATE = "2018-01-01"
END_DATE = datetime.now().strftime('%Y-%m-%d')
SEQUENCE_LENGTH = 60  # 60 days of history for prediction

print(f"Downloading data for {TICKER} from {START_DATE} to {END_DATE}")

# Download data
try:
    data = yf.download(TICKER, start=START_DATE, end=END_DATE)
    print(f"Downloaded {len(data)} days of data")
    
    # Basic data exploration
    print("\nData Overview:")
    print(data.info())
    print("\nDescriptive Statistics:")
    print(data.describe())

    # Check for missing values
    missing_values = data.isnull().sum()
    print("\nMissing Values:")
    print(missing_values)
    
    # Plot the closing prices
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'])
    plt.title(f'{TICKER} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.savefig('plots/stock_price_plot.png')
    plt.close()
    
    # Add technical indicators
    def add_technical_indicators(df):
        print("Adding technical indicators...")
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
    
    # Plot some technical indicators
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['MA20'], label='20-day MA')
    plt.plot(data['MA50'], label='50-day MA')
    plt.title(f'{TICKER} Price and Moving Averages')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(data['RSI'], label='RSI')
    plt.axhline(y=70, color='r', linestyle='--')
    plt.axhline(y=30, color='g', linestyle='--')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(data['MACD'], label='MACD')
    plt.plot(data['Signal_Line'], label='Signal Line')
    plt.title('MACD and Signal Line')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('plots/technical_indicators.png')
    plt.close()
    
    # Remove NaN values
    data.dropna(inplace=True)
    print(f"Data after removing NaN values: {len(data)} rows")
    
    # Save the preprocessed data
    data.to_csv('data/preprocessed_data.csv')
    
    # Feature selection
    features = ['Close', 'Volume', 'MA20', 'MA50', 'RSI', 'MACD', 'upper_band', 'lower_band']
    target = 'Close'
    
    # Scale the features
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data[features])
    scaled_df = pd.DataFrame(scaled_data, columns=features, index=data.index)
    
    # Create sequences for LSTM
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i+seq_length])
            y.append(data[i+seq_length, 0])  # 'Close' is the first column
        return np.array(X), np.array(y)
    
    # Create sequences
    X, y = create_sequences(scaled_data, SEQUENCE_LENGTH)
    print(f"Created {len(X)} sequences of length {SEQUENCE_LENGTH}")
    
    # Split data into training and testing sets
    split_ratio = 0.8
    split_index = int(split_ratio * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    
    print(f"Training data shape: {X_train.shape}, {y_train.shape}")
    print(f"Testing data shape: {X_test.shape}, {y_test.shape}")
    
    # Save processed data
    np.save('data/X_train.npy', X_train)
    np.save('data/y_train.npy', y_train)
    np.save('data/X_test.npy', X_test)
    np.save('data/y_test.npy', y_test)
    
    # Also save the scaler for later use
    with open('data/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Data preprocessing completed successfully!")
    print("Files saved in 'data' directory")
    
except Exception as e:
    print(f"An error occurred: {e}")
