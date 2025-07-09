"""
Advanced script for Diabetes Progression Prediction Project with hyperparameter tuning
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import joblib

# Import project modules
from utils.data_loader import load_diabetes_data
from utils.preprocessing import (
    apply_standard_scaling, 
    apply_recursive_feature_elimination,
    apply_lasso_feature_selection,
    apply_pca
)
from models.model_trainer import evaluate_model
from models.hyperparameter_tuning import (
    tune_linear_regression,
    tune_random_forest,
    tune_svr
)
from visualization.visualize import (
    plot_actual_vs_predicted,
    plot_residuals,
    plot_feature_importance,
    plot_model_comparison
)

# Create output directory for models only
os.makedirs('output/models', exist_ok=True)


def main():
    # Load data
    print("Loading diabetes dataset...")
    X_train, X_test, y_train, y_test, feature_names = load_diabetes_data()
    print(f"Dataset loaded: {X_train.shape[0]} training samples, {X_test.shape[0]} testing samples")
    
    # Preprocessing
    print("\nApplying preprocessing...")
    
    # Recursive Feature Elimination + Scaling (based on best result from main.py)
    print("Using RFE for feature selection...")
    X_train_rfe, X_test_rfe, selected_features_rfe, rfe = apply_recursive_feature_elimination(
        X_train, y_train, X_test
    )
    X_train_scaled, X_test_scaled, scaler = apply_standard_scaling(X_train_rfe, X_test_rfe)
    print(f"Selected features: {selected_features_rfe}")
    
    # Save preprocessing objects for future use
    print("Saving preprocessing objects...")
    joblib.dump(rfe, 'output/models/rfe_selector.pkl')
    joblib.dump(scaler, 'output/models/scaler.pkl')
    
    # Hyperparameter tuning
    print("\nPerforming hyperparameter tuning...")
    start_time = time.time()
    
    # Tune linear models
    try:
        linear_models = tune_linear_regression(X_train_scaled, y_train)
    except Exception as e:
        print(f"Error tuning linear models: {str(e)}")
        # Fallback to basic models
        from sklearn.linear_model import Ridge, Lasso, ElasticNet
        linear_models = {
            'Ridge': Ridge(),
            'Lasso': Lasso(),
            'ElasticNet': ElasticNet()
        }
    
    # Define a fixed random forest model to avoid parameter errors
    try:
        rf_model = tune_random_forest(X_train_scaled, y_train)
    except Exception as e:
        print(f"Error tuning Random Forest: {str(e)}")
        # Fallback to a basic model
        from sklearn.ensemble import RandomForestRegressor
        rf_model = RandomForestRegressor(n_estimators=100, max_features="sqrt", random_state=42)
        rf_model.fit(X_train_scaled, y_train)
    
    # Tune SVR
    try:
        svr_model = tune_svr(X_train_scaled, y_train)
    except Exception as e:
        print(f"Error tuning SVR: {str(e)}")
        # Fallback to a basic model
        from sklearn.svm import SVR
        svr_model = SVR(kernel='linear')
        svr_model.fit(X_train_scaled, y_train)
    
    tuning_time = time.time() - start_time
    print(f"Tuning completed in {tuning_time:.2f} seconds")
    
    # Combine all tuned models
    models = {
        'Ridge': linear_models['Ridge'],
        'Lasso': linear_models['Lasso'],
        'ElasticNet': linear_models['ElasticNet'],
        'Random Forest': rf_model,
        'SVR': svr_model
    }
    
    # Save tuned models
    print("Saving tuned models...")
    for name, model in models.items():
        joblib.dump(model, f'output/models/{name.lower().replace(" ", "_")}_tuned.pkl')
    
    # Evaluate models
    print("\nEvaluating tuned models...")
    results = {}
    predictions = {}
    
    for name, model in models.items():
        try:
            metrics, y_pred = evaluate_model(model, X_test_scaled, y_test)
            results[name] = metrics
            predictions[name] = y_pred
            
            print(f"{name}: R² = {metrics['r2']:.4f}, RMSE = {metrics['rmse']:.4f}")
        except Exception as e:
            print(f"Error evaluating {name}: {str(e)}")
    
    # Only plot and find best model if we have results
    if results:
        # Plot model comparison
        try:
            model_comparison_fig = plot_model_comparison(results)
            plt.figure(model_comparison_fig.number)
            plt.show()
        except Exception as e:
            print(f"Error plotting model comparison: {str(e)}")
        
        # Find best model
        best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
        best_model = models[best_model_name]
        best_model_pred = predictions[best_model_name]
        
        print(f"\nBest model: {best_model_name} with R² = {results[best_model_name]['r2']:.4f}")
        
        # Plot actual vs predicted for best model
        try:
            actual_vs_pred_fig = plot_actual_vs_predicted(y_test, best_model_pred, best_model_name)
            plt.figure(actual_vs_pred_fig.number)
            plt.show()
        except Exception as e:
            print(f"Error plotting actual vs predicted: {str(e)}")
        
        # Plot residuals for best model
        try:
            residuals_fig = plot_residuals(y_test, best_model_pred, best_model_name)
            plt.figure(residuals_fig.number)
            plt.show()
        except Exception as e:
            print(f"Error plotting residuals: {str(e)}")
        
        # Try to plot feature importance for best model
        try:
            # If we have selected features, use them; otherwise use all feature names
            features_to_plot = selected_features_rfe if selected_features_rfe else feature_names
            feature_importance_fig = plot_feature_importance(best_model, features_to_plot, best_model_name)
            plt.figure(feature_importance_fig.number)
            plt.show()
        except Exception as e:
            print(f"Could not generate feature importance plot: {str(e)}")
    else:
        print("No valid model evaluations to compare")
    
    print("\nAdvanced analysis complete.")
    print("Models saved to 'output/models' directory.")


if __name__ == "__main__":
    main()