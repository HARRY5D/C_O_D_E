"""
Data Loader Module for Diabetes Prediction Project
Loads and prepares the diabetes dataset
"""

import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split


def load_diabetes_data(test_size=0.1, random_state=45):
    """
    Load the diabetes dataset and split into train and test sets
    
    Parameters:
    -----------
    test_size: float
        Proportion of data to use for testing (default: 0.1)
    random_state: int
        Random seed for reproducible results (default: 45)
        
    Returns:
    --------
    X_train, X_test, y_train, y_test: DataFrames and Series
        Split training and test data
    feature_names: list
        Names of the features in the dataset
    """
    # Load dataset
    diabetes = load_diabetes()
    X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
    y = pd.Series(diabetes.target, name="target")
    
    # Split before feature selection to avoid data leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    return X_train, X_test, y_train, y_test, diabetes.feature_names