"""
Model Training and Evaluation for Diabetes Progression Prediction Project
This module handles model training, evaluation, and model comparison.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score
import joblib
import os

def train_linear_model(X_train, y_train):
    """
    Train a Linear Regression model.
    
    Args:
        X_train (array-like): Training features
        y_train (array-like): Training target
        
    Returns:
        model (LinearRegression): Trained model
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the performance of a regression model.
    
    Args:
        model: Trained model
        X_test (array-like): Testing features
        y_test (array-like): Testing target
        
    Returns:
        metrics (dict): Dictionary containing evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    metrics = {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2,
        'predictions': y_pred
    }
    
    return metrics

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Train and evaluate multiple regression models.
    
    Args:
        X_train (array-like): Training features
        X_test (array-like): Testing features
        y_train (array-like): Training target
        y_test (array-like): Testing target
        
    Returns:
        results (dict): Dictionary with model performances
        best_model (str): Name of the best performing model
        models (dict): Dictionary containing the trained models
    """
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(),
        "Lasso": Lasso(),
        "ElasticNet": ElasticNet(),
        "SVR": SVR(),
        "Random Forest": RandomForestRegressor(random_state=42)
    }
    
    results = {}
    best_r2 = -float('inf')
    best_model = None
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Store results
        results[name] = {
            'R2': round(r2, 4),
            'RMSE': round(rmse, 4),
            'predictions': y_pred
        }
        
        # Track best model
        if r2 > best_r2:
            best_r2 = r2
            best_model = name
            
        print(f"{name} Performance:")
        print(f"R^2 Score: {r2:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print("-" * 30)
    
    return results, best_model, models

def perform_cross_validation(model, X, y, cv=6, scoring='r2'):
    """
    Perform cross-validation on a model.
    
    Args:
        model: Model to evaluate
        X (array-like): Features
        y (array-like): Target
        cv (int): Number of folds
        scoring (str): Scoring metric
        
    Returns:
        cv_results (dict): Cross-validation results
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    
    cv_results = {
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'all_scores': scores
    }
    
    print(f"Cross-Validation ({cv} folds):")
    print(f"Average {scoring}: {scores.mean():.4f}")
    print(f"Std Dev: {scores.std():.4f}")
    
    return cv_results

def save_model(model, filename, directory='models'):
    """
    Save a trained model to disk.
    
    Args:
        model: Trained model to save
        filename (str): Name for the saved model
        directory (str): Directory to save the model in
        
    Returns:
        path (str): Path where the model was saved
    """
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Save the model
    path = os.path.join(directory, filename)
    joblib.dump(model, path)
    print(f"Model saved to {path}")
    
    return path

def load_model(path):
    """
    Load a trained model from disk.
    
    Args:
        path (str): Path to the saved model
        
    Returns:
        model: The loaded model
    """
    model = joblib.load(path)
    print(f"Model loaded from {path}")
    
    return model
