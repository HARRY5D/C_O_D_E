"""
Preprocessing Utilities for Diabetes Progression Prediction Project
This module handles feature scaling, feature selection, and other preprocessing tasks.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE, SelectKBest, f_regression
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.decomposition import PCA

def scale_features(X_train, X_test):
    """
    Standardize features by removing the mean and scaling to unit variance.
    
    Args:
        X_train (array-like): Training data
        X_test (array-like): Testing data
        
    Returns:
        X_train_scaled (np.ndarray): Scaled training data
        X_test_scaled (np.ndarray): Scaled testing data
        scaler (StandardScaler): The fitted scaler
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, scaler

def select_features_rfe(X_train, X_test, y_train, feature_names, n_features=6):
    """
    Select features using Recursive Feature Elimination (RFE).
    
    Args:
        X_train (array-like): Training data
        X_test (array-like): Testing data
        y_train (array-like): Training targets
        feature_names (list): Names of the features
        n_features (int): Number of features to select
        
    Returns:
        X_train_selected (np.ndarray): Training data with selected features
        X_test_selected (np.ndarray): Testing data with selected features
        selected_features (list): Names of selected features
        selector (RFE): Fitted RFE selector
    """
    estimator = LinearRegression()
    selector = RFE(estimator=estimator, n_features_to_select=n_features)
    
    X_train_selected = selector.fit_transform(X_train, y_train)
    X_test_selected = selector.transform(X_test)
    
    selected_features = [feature_names[i] for i, selected in enumerate(selector.support_) if selected]
    print(f"Selected features (RFE): {selected_features}")
    
    return X_train_selected, X_test_selected, selected_features, selector

def select_features_kbest(X_train, X_test, y_train, feature_names, k=6):
    """
    Select features using SelectKBest with f_regression score function.
    
    Args:
        X_train (array-like): Training data
        X_test (array-like): Testing data
        y_train (array-like): Training targets
        feature_names (list): Names of the features
        k (int): Number of features to select
        
    Returns:
        X_train_selected (np.ndarray): Training data with selected features
        X_test_selected (np.ndarray): Testing data with selected features
        selected_features (list): Names of selected features
        selector (SelectKBest): Fitted SelectKBest selector
    """
    selector = SelectKBest(score_func=f_regression, k=k)
    
    X_train_selected = selector.fit_transform(X_train, y_train)
    X_test_selected = selector.transform(X_test)
    
    selected_features = [feature_names[i] for i, selected in enumerate(selector.get_support()) if selected]
    print(f"Selected features (KBest): {selected_features}")
    
    return X_train_selected, X_test_selected, selected_features, selector

def select_features_lasso(X_train, X_test, y_train, feature_names, cv=5):
    """
    Select features using LassoCV for automatic feature selection.
    
    Args:
        X_train (array-like): Training data
        X_test (array-like): Testing data
        y_train (array-like): Training targets
        feature_names (list): Names of the features
        cv (int): Number of cross-validation folds
        
    Returns:
        X_train_selected (np.ndarray): Training data with selected features
        X_test_selected (np.ndarray): Testing data with selected features
        selected_features (list): Names of selected features
        selector (LassoCV): Fitted LassoCV selector
    """
    selector = LassoCV(cv=cv)
    selector.fit(X_train, y_train)
    
    # Get feature mask
    feature_mask = selector.coef_ != 0
    
    # Apply mask
    X_train_selected = X_train[:, feature_mask]
    X_test_selected = X_test[:, feature_mask]
    
    selected_features = [feature_names[i] for i, selected in enumerate(feature_mask) if selected]
    print(f"Selected features (Lasso): {selected_features}")
    
    return X_train_selected, X_test_selected, selected_features, selector

def apply_pca(X_train, X_test, n_components=0.95):
    """
    Apply Principal Component Analysis (PCA) for dimensionality reduction.
    
    Args:
        X_train (array-like): Training data (should be standardized)
        X_test (array-like): Testing data (should be standardized)
        n_components (float or int): Number of components to keep
            If float: proportion of variance to retain
            If int: number of components to keep
            
    Returns:
        X_train_pca (np.ndarray): PCA-transformed training data
        X_test_pca (np.ndarray): PCA-transformed testing data
        pca (PCA): Fitted PCA transformer
    """
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    
    if isinstance(n_components, float):
        print(f"PCA: Using {pca.n_components_} components to explain {n_components*100:.1f}% of variance")
    else:
        explained_variance = pca.explained_variance_ratio_.sum()
        print(f"PCA: Using {n_components} components explains {explained_variance*100:.1f}% of variance")
        
    return X_train_pca, X_test_pca, pca
