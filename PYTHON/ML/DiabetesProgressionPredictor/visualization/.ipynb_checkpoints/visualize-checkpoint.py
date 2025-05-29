"""
Visualization Module for Diabetes Prediction Project
Provides functions for visualizing data and model results
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_actual_vs_predicted(y_test, y_pred, model_name='Model'):
    """
    Create a scatter plot of actual vs predicted values
    
    Parameters:
    -----------
    y_test: array-like
        True target values
    y_pred: array-like
        Predicted target values
    model_name: str
        Name of the model for the plot title
        
    Returns:
    --------
    fig: matplotlib Figure
        The created figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(y_test, y_pred, alpha=0.7)
    
    # Add the perfect prediction line
    min_val = min(min(y_test), min(y_pred))
    max_val = max(max(y_test), max(y_pred))
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2)
    
    ax.set_xlabel('Actual Values')
    ax.set_ylabel('Predicted Values')
    ax.set_title(f'Actual vs Predicted Values - {model_name}')
    ax.grid(True, alpha=0.3)
    
    # Add R² annotation
    r2 = np.corrcoef(y_test, y_pred)[0, 1]**2
    ax.annotate(f'R² = {r2:.4f}', xy=(0.05, 0.95), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    plt.tight_layout()
    return fig


def plot_residuals(y_test, y_pred, model_name='Model'):
    """
    Create a residual plot
    
    Parameters:
    -----------
    y_test: array-like
        True target values
    y_pred: array-like
        Predicted target values
    model_name: str
        Name of the model for the plot title
        
    Returns:
    --------
    fig: matplotlib Figure
        The created figure
    """
    residuals = y_test - y_pred
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(y_pred, residuals, alpha=0.7)
    ax.axhline(y=0, color='r', linestyle='-', lw=2)
    
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Residuals')
    ax.set_title(f'Residual Plot - {model_name}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_feature_importance(model, feature_names, model_name='Model'):
    """
    Create a bar plot of feature importance
    
    Parameters:
    -----------
    model: estimator
        Trained model with feature_importances_ attribute or coef_ attribute
    feature_names: list
        Names of the features
    model_name: str
        Name of the model for the plot title
        
    Returns:
    --------
    fig: matplotlib Figure
        The created figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    try:
        # Try to get feature importances
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)  # Take absolute values for linear models
        else:
            raise ValueError("Model does not have feature_importances_ or coef_ attribute")
        
        # Sort features by importance
        indices = np.argsort(importances)
        
        # Plot
        ax.barh(np.array(feature_names)[indices], importances[indices])
        ax.set_xlabel('Feature Importance')
        ax.set_title(f'Feature Importance - {model_name}')
        ax.grid(True, alpha=0.3)
        
    except Exception as e:
        plt.close(fig)  # Close the figure if plotting fails
        print(f"Could not plot feature importance: {str(e)}")
        return None
    
    plt.tight_layout()
    return fig


def plot_model_comparison(results, metric='r2', ascending=False):
    """
    Create a bar plot comparing models based on the specified metric
    
    Parameters:
    -----------
    results: dict
        Dictionary with model names as keys and metrics dictionaries as values
    metric: str
        Metric to compare (default: 'r2')
    ascending: bool
        Whether to sort in ascending order (default: False)
        
    Returns:
    --------
    fig: matplotlib Figure
        The created figure
    """
    if not results:
        return None
    
    # Extract metric values for each model
    model_names = list(results.keys())
    metric_values = [results[model][metric] for model in model_names]
    
    # Sort for better visualization
    sorted_indices = np.argsort(metric_values)
    if not ascending:
        sorted_indices = sorted_indices[::-1]  # Reverse for descending
    
    sorted_names = [model_names[i] for i in sorted_indices]
    sorted_values = [metric_values[i] for i in sorted_indices]
    
    # Create bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(sorted_names, sorted_values, color='steelblue')
    
    # Add values to bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + (max(sorted_values) * 0.01), 
                bar.get_y() + bar.get_height() / 2,
                f'{sorted_values[i]:.4f}',
                va='center')
    
    # Labels and title
    ax.set_xlabel(f'Performance ({metric})')
    ax.set_title(f'Model Comparison - {metric.upper()}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_correlation_matrix(X, feature_names=None):
    """
    Create a correlation matrix heatmap
    
    Parameters:
    -----------
    X: DataFrame or array-like
        Feature matrix
    feature_names: list, optional
        Names of the features (used if X is not a DataFrame)
        
    Returns:
    --------
    fig: matplotlib Figure
        The created figure
    """
    # Convert to DataFrame if necessary
    if not isinstance(X, pd.DataFrame):
        if feature_names is None:
            feature_names = [f"Feature {i+1}" for i in range(X.shape[1])]
        X = pd.DataFrame(X, columns=feature_names)
    
    # Calculate correlation matrix
    corr_matrix = X.corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', 
                linewidths=0.5, vmin=-1, vmax=1, ax=ax)
    ax.set_title('Feature Correlation Matrix')
    
    plt.tight_layout()
    return fig
