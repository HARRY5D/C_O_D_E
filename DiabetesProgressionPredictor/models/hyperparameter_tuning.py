from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np

def tune_random_forest(X_train, y_train):
    """
    Tune hyperparameters for Random Forest using GridSearchCV.
    
    Args:
        X_train (array-like): Training features
        y_train (array-like): Training target
        
    Returns:
        model: Tuned Random Forest model
    """
    print("Tuning Random Forest...")
    
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None],  # Removed 'auto' as it's no longer supported
        'bootstrap': [True, False]
    }
    
    # Create model
    rf = RandomForestRegressor(random_state=42)
    
    # Grid search
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        error_score=np.nan  # Return NaN instead of raising error for failed fits
    )
    
    grid_search.fit(X_train, y_train)
    
    # Print results
    print(f"  Best parameters: {grid_search.best_params_}")
    print(f"  Best score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_