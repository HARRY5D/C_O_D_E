"""
Data Loader for Diabetes Progression Prediction Project
This module handles loading and preprocessing the Diabetes dataset.
"""
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

def load_diabetes_data():
    """
    Load the Diabetes dataset from scikit-learn.
    
    Returns:
        X (pd.DataFrame): Features
        y (pd.Series): Target variable
        dataset (Bunch): Full dataset object
    """
    dataset = load_diabetes()
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = pd.Series(dataset.target, name="target")
    
    # Print dataset description
    print("Dataset Info:")
    print(f"Number of samples: {X.shape[0]}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Feature names: {dataset.feature_names}")
    print(f"Target description: {dataset.DESCR.split('Target')[1].split('**')[0].strip()}")
    
    return X, y, dataset

def split_data(X, y, test_size=0.1, random_state=42):
    """
    Split data into training and testing sets.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target variable
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
        
    Returns:
        X_train, X_test, y_train, y_test: Split datasets
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"Training set size: {X_train.shape[0]} samples")
    print(f"Testing set size: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test the module
    X, y, _ = load_diabetes_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
