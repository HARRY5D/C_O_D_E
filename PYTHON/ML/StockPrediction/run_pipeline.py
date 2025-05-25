"""
Stock Price Prediction - Main Runner
This script runs the complete stock price prediction pipeline
"""

import os
import time
import subprocess
import argparse

def run_process(script_name, description):
    """Run a Python script and return the exit code"""
    print(f"\n{'='*80}")
    print(f"Running {description}...")
    print(f"{'='*80}")
    
    start_time = time.time()
    process = subprocess.run(['python', script_name])
    end_time = time.time()
    
    print(f"\nCompleted in {(end_time - start_time):.2f} seconds")
    return process.returncode

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run stock price prediction pipeline')
    parser.add_argument('--ticker', default='AAPL', help='Stock ticker symbol (default: AAPL)')
    parser.add_argument('--days', type=int, default=30, help='Number of days to predict (default: 30)')
    args = parser.parse_args()
    
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Save ticker to a file for other scripts to use
    with open('data/config.txt', 'w') as f:
        f.write(f"TICKER={args.ticker}\n")
        f.write(f"DAYS={args.days}\n")
    
    print(f"\nStock Price Prediction Pipeline")
    print(f"Ticker: {args.ticker}")
    print(f"Prediction Days: {args.days}")
    
    # Run data preprocessing
    if run_process('data_preprocessing.py', 'Data Preprocessing') != 0:
        print("Data preprocessing failed. Stopping pipeline.")
        return
    
    # Run ARIMA model
    if run_process('arima_model.py', 'ARIMA Model Training and Evaluation') != 0:
        print("ARIMA model failed. Stopping pipeline.")
        return
    
    # Run LSTM model
    if run_process('lstm_model.py', 'LSTM Model Training and Evaluation') != 0:
        print("LSTM model failed. Stopping pipeline.")
        return
    
    # Run model comparison
    if run_process('model_comparison.py', 'Model Comparison') != 0:
        print("Model comparison failed. Stopping pipeline.")
        return
    
    # Run prediction for the specified ticker
    print(f"\n{'='*80}")
    print(f"Making predictions for {args.ticker} for the next {args.days} days...")
    print(f"{'='*80}")
    
    # Construct and run the prediction command
    prediction_command = ['python', 'predict.py']
    process = subprocess.run(prediction_command)
    
    if process.returncode == 0:
        print(f"\nPrediction completed successfully!")
        print(f"Check the 'results' folder for prediction outputs.")
    else:
        print("\nPrediction failed.")
    
    print("\nStock Price Prediction Pipeline completed!")

if __name__ == "__main__":
    main()
