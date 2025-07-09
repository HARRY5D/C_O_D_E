"""
Model Module for Diabetes Prediction Project
Defines and trains different regression models
"""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score


class ModelFactory:
    """
    Factory class for creating and managing regression models
    """
    @staticmethod
    def get_model(model_name):
        """
        Get model instance based on the model name
        
        Parameters:
        -----------
        model_name: str
            Name of the model to create
            
        Returns:
        --------
        model: estimator
            Scikit-learn compatible estimator
        """
        models = {
            'linear_regression': LinearRegression(),
            'ridge': Ridge(),
            'lasso': Lasso(),
            'elastic_net': ElasticNet(), 
            'svr': SVR(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        if model_name in models:
            return models[model_name]
        else:
            raise ValueError(f"Unknown model: {model_name}")


def train_model(model, X_train, y_train):
    """
    Train the model on the given data
    
    Parameters:
    -----------
    model: estimator
        Model to train
    X_train: array or DataFrame
        Training features
    y_train: array or Series
        Training target values
        
    Returns:
    --------
    model: estimator
        Trained model
    """
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on the test data
    
    Parameters:
    -----------
    model: estimator
        Trained model
    X_test: array or DataFrame
        Test features
    y_test: array or Series
        Test target values
        
    Returns:
    --------
    metrics: dict
        Dictionary with evaluation metrics
    y_pred: array
        Predicted values
    """
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'mse': mse,
        'rmse': rmse,
        'r2': r2
    }
    
    return metrics, y_pred


def evaluate_multiple_models(models_dict, X_train, y_train, X_test, y_test):
    """
    Train and evaluate multiple models
    
    Parameters:
    -----------
    models_dict: dict
        Dictionary of model name to model instance
    X_train: array or DataFrame
        Training features
    y_train: array or Series
        Training target values
    X_test: array or DataFrame
        Test features
    y_test: array or Series
        Test target values
        
    Returns:
    --------
    results: dict
        Dictionary with model names as keys and evaluation metrics as values
    predictions: dict
        Dictionary with model names as keys and predictions as values
    trained_models: dict
        Dictionary with model names as keys and trained models as values
    """
    results = {}
    predictions = {}
    trained_models = {}
    
    for name, model in models_dict.items():
        # Train the model
        trained_model = train_model(model, X_train, y_train)
        trained_models[name] = trained_model
        
        # Evaluate the model
        metrics, y_pred = evaluate_model(trained_model, X_test, y_test)
        results[name] = metrics
        predictions[name] = y_pred
    
    return results, predictions, trained_models