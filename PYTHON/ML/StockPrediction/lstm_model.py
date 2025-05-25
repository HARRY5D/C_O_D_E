"""
Stock Price Prediction - LSTM Model
This script builds an LSTM deep learning model for stock price prediction
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Create directories if they don't exist
os.makedirs('plots', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Check for GPU
print("Checking for GPU...")
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPU is available: {gpus}")
    # Set memory growth to avoid OOM errors
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
else:
    print("No GPU available, using CPU instead")

# Load preprocessed data
print("Loading preprocessed data...")
try:
    X_train = np.load('data/X_train.npy')
    y_train = np.load('data/y_train.npy')
    X_test = np.load('data/X_test.npy')
    y_test = np.load('data/y_test.npy')
    
    # Load scaler for inverse transformation
    with open('data/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
        
    # Load original data for plotting
    data = pd.read_csv('data/preprocessed_data.csv', index_col=0, parse_dates=True)
    
    print(f"Training data shape: {X_train.shape}, {y_train.shape}")
    print(f"Testing data shape: {X_test.shape}, {y_test.shape}")
    
    # Build LSTM model
    print("\nBuilding LSTM model...")
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    # Compile model
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.summary()
    
    # Callbacks
    early_stop = EarlyStopping(monitor='val_loss', patience=10)
    checkpoint = ModelCheckpoint('models/lstm_checkpoint.h5', save_best_only=True, monitor='val_loss')
    
    # Train model
    print("\nTraining model...")
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )
    
    # Plot training history
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('LSTM Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/lstm_training_history.png')
    plt.close()
    
    # Evaluate model
    print("\nEvaluating model...")
    train_loss = model.evaluate(X_train, y_train, verbose=0)
    test_loss = model.evaluate(X_test, y_test, verbose=0)
    print(f"Train Loss: {train_loss:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Inverse transform the predictions to original scale
    # Create arrays with zeros for all features except the target
    y_pred_inverse = np.zeros((len(y_pred), X_train.shape[2]))
    y_pred_inverse[:, 0] = y_pred.flatten()  # First column is 'Close'
    
    y_test_inverse = np.zeros((len(y_test), X_train.shape[2]))
    y_test_inverse[:, 0] = y_test  # First column is 'Close'
    
    # Inverse transform
    y_pred_original = scaler.inverse_transform(y_pred_inverse)[:, 0]
    y_test_original = scaler.inverse_transform(y_test_inverse)[:, 0]
    
    # Calculate metrics
    rmse = math.sqrt(mean_squared_error(y_test_original, y_pred_original))
    mae = mean_absolute_error(y_test_original, y_pred_original)
    mape = np.mean(np.abs((y_test_original - y_pred_original) / y_test_original)) * 100
    
    print(f"\nModel Evaluation Metrics:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"MAPE: {mape:.2f}%")
    
    # Plot results
    # Get the dates for the test data
    split_ratio = 0.8
    split_index = int(split_ratio * len(data))
    
    # The test data starts 'sequence_length' indices after the split point because of how sequences are created
    sequence_length = X_train.shape[1]
    test_start_idx = split_index + sequence_length
    test_data = data.iloc[test_start_idx:]
    test_dates = test_data.index[:len(y_test_original)]
    
    plt.figure(figsize=(12, 6))
    plt.plot(test_dates, y_test_original, label='Actual')
    plt.plot(test_dates, y_pred_original, label='Predicted', color='red')
    plt.title('LSTM: Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/lstm_prediction.png')
    plt.close()
    
    # Save predictions for later comparison
    predictions_df = pd.DataFrame({
        'Date': test_dates,
        'Actual': y_test_original,
        'Predicted': y_pred_original
    }).set_index('Date')
    
    predictions_df.to_csv('data/lstm_predictions.csv')
    
    # Save the model
    model.save('models/lstm_model.h5')
    
    # Make future predictions (next 30 days)
    print("\nMaking future predictions (next 30 days)...")
    future_days = 30
    
    # Use the last sequence from our test data
    last_sequence = X_test[-1:].copy()
    lstm_future = []
    
    # Predict one day at a time and update the sequence
    for _ in range(future_days):
        # Make prediction with current sequence
        next_pred = model.predict(last_sequence)
        lstm_future.append(next_pred[0, 0])
        
        # Create a new sequence by:
        # 1. Dropping the first time step
        # 2. Appending the new prediction
        last_seq = last_sequence[0]
        new_seq = np.append(last_seq[1:, :], [[next_pred[0, 0]] + [0] * (last_seq.shape[1]-1)], axis=0)
        last_sequence[0] = new_seq
    
    # Scale back the predictions
    lstm_future_array = np.array(lstm_future).reshape(-1, 1)
    lstm_future_full = np.zeros((len(lstm_future), X_train.shape[2]))
    lstm_future_full[:, 0] = lstm_future_array.flatten()
    lstm_future_original = scaler.inverse_transform(lstm_future_full)[:, 0]
    
    # Create future dates
    future_dates = pd.date_range(start=test_dates[-1], periods=future_days+1)[1:]
    
    # Save future predictions
    future_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Price': lstm_future_original
    }).set_index('Date')
    
    future_df.to_csv('data/lstm_future_predictions.csv')
    
    # Plot future predictions
    plt.figure(figsize=(12, 6))
    plt.plot(test_dates[-60:], y_test_original[-60:], label='Historical Data')
    plt.plot(future_dates, lstm_future_original, label='LSTM Forecast', color='green', linestyle='--')
    plt.title('LSTM: Future Stock Price Forecast (Next 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/lstm_future_forecast.png')
    plt.close()
    
    print("\nLSTM model completed successfully!")
    print("Results saved in 'plots' and 'models' directories")
    
except Exception as e:
    print(f"An error occurred: {e}")
