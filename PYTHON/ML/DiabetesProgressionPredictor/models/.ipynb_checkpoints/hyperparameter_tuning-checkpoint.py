"""
Hyperparameter Tuning Module for Diabetes Prediction Project
Provides functions for hyperparameter optimization
"""

import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import make_scorer, mean_squared_error, r2_score


def rmse_scorer():
    """
    Create an RMSE scorer for grid search
    
    Returns:
    --------
    scorer: callable
        Sklearn-compatible scorer function
    """
    return make_scorer(
        lambda y_true, y_pred: -np.sqrt(mean_squared_error(y_true, y_pred)),  # Negative for maximization
        greater_is_better=False
    )


def r2_scorer():
    """
    Create an R² scorer for grid search
    
    Returns:
    --------
    scorer: callable
        Sklearn-compatible scorer function
    """
    return make_scorer(r2_score, greater_is_better=True)


def tune_linear_regression(X_train, y_train, cv=5):
    """
    Tune hyperparameters for Ridge/Lasso/ElasticNet regression models
    
    Parameters:
    -----------
    X_train: array or DataFrame
        Training features
    y_train: array or Series
        Training target values
    cv: int
        Number of cross-validation folds
        
    Returns:
    --------
    best_models: dict
        Dictionary containing the best tuned models
    """
    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    
    # Define parameter grids
    ridge_params = {
        'alpha': np.logspace(-3, 3, 7),
        'fit_intercept': [True, False],
        'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
    }
    
    lasso_params = {
        'alpha': np.logspace(-3, 3, 7),
        'fit_intercept': [True, False],
        'selection': ['cyclic', 'random']
    }
    
    elasticnet_params = {
        'alpha': np.logspace(-3, 3, 7),
        'l1_ratio': np.linspace(0.1, 0.9, 9),
        'fit_intercept': [True, False],
        'selection': ['cyclic', 'random']
    }
    
    # Configure grid search
    scorer = r2_scorer()
    
    # Dictionary to hold model names and configurations
    models = {
        'Ridge': (Ridge(), ridge_params),
        'Lasso': (Lasso(), lasso_params),
        'ElasticNet': (ElasticNet(), elasticnet_params)
    }
    
    best_models = {}
    
    # Perform grid search for each model
    for name, (model, param_grid) in models.items():
        print(f"Tuning {name}...")
        grid_search = GridSearchCV(
            model, param_grid, scoring=scorer, cv=cv, n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        best_models[name] = grid_search.best_estimator_
        
        print(f"  Best parameters: {grid_search.best_params_}")
        print(f"  Best score: {grid_search.best_score_:.4f}")
    
    return best_models


def tune_random_forest(X_train, y_train, cv=5):
    """
    Tune hyperparameters for Random Forest regressor
    
    Parameters:
    -----------
    X_train: array or DataFrame
        Training features
    y_train: array or Series
        Training target values
    cv: int
        Number of cross-validation folds
        
    Returns:
    --------
    best_model: RandomForestRegressor
        The best tuned model
    """
    from sklearn.ensemble import RandomForestRegressor
    
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }
    
    # Configure randomized search for efficiency
    scorer = r2_scorer()
    random_search = RandomizedSearchCV(
        RandomForestRegressor(random_state=42), 
        param_distributions=param_grid,
        n_iter=20,  # Number of parameter settings sampled
        scoring=scorer,
        cv=cv,
        n_jobs=-1,
        random_state=42
    )
    
    print("Tuning Random Forest...")
    random_search.fit(X_train, y_train)
    
    print(f"  Best parameters: {random_search.best_params_}")
    print(f"  Best score: {random_search.best_score_:.4f}")
    
    return random_search.best_estimator_


def tune_svr(X_train, y_train, cv=5):
    """
    Tune hyperparameters for SVR
    
    Parameters:
    -----------
    X_train: array or DataFrame
        Training features
    y_train: array or Series
        Training target values
    cv: int
        Number of cross-validation folds
        
    Returns:
    --------
    best_model: SVR
        The best tuned model
    """
    from sklearn.svm import SVR
    
    # Define parameter grid
    param_grid = {
        'C': np.logspace(-3, 3, 7),
        'gamma': np.logspace(-4, 0, 5),
        'kernel': ['linear', 'rbf', 'poly'],
        'epsilon': [0.01, 0.1, 0.2]
    }
    
    # Configure randomized search for efficiency
    scorer = r2_scorer()
    random_search = RandomizedSearchCV(
        SVR(), 
        param_distributions=param_grid,
        n_iter=20,  # Number of parameter settings sampled
        scoring=scorer,
        cv=cv,
        n_jobs=-1,
        random_state=42
    )
    
    print("Tuning SVR...")
    random_search.fit(X_train, y_train)
    
    print(f"  Best parameters: {random_search.best_params_}")
    print(f"  Best score: {random_search.best_score_:.4f}")
    
    return random_search.best_estimator_
