"""
Script for making predictions using a saved model
"""

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_model_and_preprocessors(model_path='output/models/random_forest_tuned.pkl',
                                rfe_path='output/models/rfe_selector.pkl',
                                scaler_path='output/models/scaler.pkl'):
    """
    Load the saved model and preprocessors
    
    Returns:
    --------
    model: estimator
        The trained model
    rfe: RFE
        The RFE feature selector
    scaler: StandardScaler
        The scaler for features
    """
    try:
        model = joblib.load(model_path)
        rfe = joblib.load(rfe_path)
        scaler = joblib.load(scaler_path)
        return model, rfe, scaler
    except FileNotFoundError as e:
        print(f"Error loading model or preprocessors: {str(e)}")
        print("Make sure you've run advanced.py first to train and save the models.")
        exit(1)


def predict_progression(features, model, rfe, scaler):
    """
    Make a prediction for a single patient
    
    Parameters:
    -----------
    features: array-like
        The patient features
    model: estimator
        The trained model
    rfe: RFE
        The RFE feature selector
    scaler: StandardScaler
        The scaler for features
        
    Returns:
    --------
    prediction: float
        The predicted disease progression
    """
    # Apply feature selection
    features_rfe = rfe.transform(features)
    
    # Apply scaling
    features_scaled = scaler.transform(features_rfe)
    
    # Make prediction
    prediction = model.predict(features_scaled)
    
    return prediction[0]


def predict_from_user_input(model, rfe, scaler):
    """
    Prompt user for features and make prediction
    
    Parameters:
    -----------
    model: estimator
        The trained model
    rfe: RFE
        The RFE feature selector
    scaler: StandardScaler
        The scaler for features
    """
    from sklearn.datasets import load_diabetes
    
    # Get feature names from the diabetes dataset
    diabetes = load_diabetes()
    feature_names = diabetes.feature_names
    
    print("\n===== Diabetes Progression Predictor =====")
    print("Please enter patient information:")
    
    # Create a dictionary to store features
    features = {}
    
    for name in feature_names:
        while True:
            try:
                value = float(input(f"{name}: "))
                features[name] = value
                break
            except ValueError:
                print("Please enter a valid number.")
    
    # Convert to DataFrame (same format as training data)
    patient_data = pd.DataFrame([features])
    
    # Make prediction
    progression = predict_progression(patient_data, model, rfe, scaler)
    
    print("\n=== Prediction ===")
    print(f"Predicted disease progression: {progression:.2f}")
    print("Note: Higher values indicate more severe disease progression.")


def main():
    # Load model and preprocessors
    print("Loading model and preprocessors...")
    model, rfe, scaler = load_model_and_preprocessors()
    print("Model loaded successfully!")
    
    # Make predictions from user input
    while True:
        predict_from_user_input(model, rfe, scaler)
        
        # Ask if the user wants to make another prediction
        another = input("\nMake another prediction? (y/n): ").lower()
        if another != 'y':
            break


if __name__ == "__main__":
    main()
