"""
Main script for Diabetes Progression Prediction Project
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Import project modules
from utils.data_loader import load_diabetes_data
from utils.preprocessing import (
    apply_standard_scaling, 
    apply_recursive_feature_elimination,
    apply_lasso_feature_selection,
    apply_select_k_best,
    apply_pca
)
from models.model_trainer import ModelFactory, evaluate_multiple_models
from visualization.visualize import (
    plot_actual_vs_predicted,
    plot_residuals,
    plot_feature_importance,
    plot_model_comparison,
    plot_correlation_matrix
)

# Create output directory for figures
os.makedirs('output', exist_ok=True)


def main():
    # Load data
    print("Loading diabetes dataset...")
    X_train, X_test, y_train, y_test, feature_names = load_diabetes_data()
    print(f"Dataset loaded: {X_train.shape[0]} training samples, {X_test.shape[0]} testing samples")
    print(f"Features: {feature_names}")
    
    # Plot correlation matrix
    print("\nGenerating correlation matrix...")
    fig_corr = plot_correlation_matrix(X_train)
    fig_corr.savefig('output/correlation_matrix.png')
    
    # Preprocessing options
    print("\nApplying preprocessing methods...")
    
    # 1. Standard scaling only
    X_train_scaled, X_test_scaled, _ = apply_standard_scaling(X_train, X_test)
    
    # 2. Recursive Feature Elimination + Scaling
    X_train_rfe, X_test_rfe, selected_features_rfe, rfe = apply_recursive_feature_elimination(
        X_train, y_train, X_test
    )
    X_train_rfe_scaled, X_test_rfe_scaled, _ = apply_standard_scaling(X_train_rfe, X_test_rfe)
    print(f"RFE selected features: {selected_features_rfe}")
    
    # 3. Lasso feature selection + Scaling
    X_train_lasso, X_test_lasso, selected_features_lasso, _ = apply_lasso_feature_selection(
        X_train, y_train, X_test
    )
    X_train_lasso_scaled, X_test_lasso_scaled, _ = apply_standard_scaling(X_train_lasso, X_test_lasso)
    print(f"Lasso selected features: {selected_features_lasso}")
    
    # 4. SelectKBest feature selection + Scaling
    X_train_kbest, X_test_kbest, selected_features_kbest, _ = apply_select_k_best(
        X_train, y_train, X_test
    )
    X_train_kbest_scaled, X_test_kbest_scaled, _ = apply_standard_scaling(X_train_kbest, X_test_kbest)
    print(f"SelectKBest selected features: {selected_features_kbest}")
    
    # Prepare model dictionary - using only LinearRegression for this example
    print("\nCreating models...")
    model_factory = ModelFactory()
    
    # Evaluate with different preprocessing approaches
    preprocessing_approaches = {
        'All Features (Scaled)': (X_train_scaled, X_test_scaled, feature_names),
        'RFE (Scaled)': (X_train_rfe_scaled, X_test_rfe_scaled, selected_features_rfe),
        'Lasso (Scaled)': (X_train_lasso_scaled, X_test_lasso_scaled, selected_features_lasso),
        'SelectKBest (Scaled)': (X_train_kbest_scaled, X_test_kbest_scaled, selected_features_kbest)
    }
    
    # Compare different models with the best preprocessing approach
    best_approach = 'RFE (Scaled)'  # We'll determine this as we go
    best_r2 = -float('inf')
    best_approach_data = preprocessing_approaches[best_approach]
    
    # First, evaluate linear regression with different preprocessing approaches
    print("\nEvaluating linear regression with different preprocessing methods...")
    preprocessing_results = {}
    
    for approach_name, (X_train_proc, X_test_proc, _) in preprocessing_approaches.items():
        model = model_factory.get_model('linear_regression')
        results, _, _ = evaluate_multiple_models(
            {'Linear Regression': model}, 
            X_train_proc, y_train, X_test_proc, y_test
        )
        r2 = results['Linear Regression']['r2']
        rmse = results['Linear Regression']['rmse']
        
        preprocessing_results[approach_name] = {'r2': r2, 'rmse': rmse}
        print(f"{approach_name}: R² = {r2:.4f}, RMSE = {rmse:.4f}")
        
        # Track best preprocessing approach
        if r2 > best_r2:
            best_r2 = r2
            best_approach = approach_name
            best_approach_data = (X_train_proc, X_test_proc, _)
    
    # Plot preprocessing comparison
    preprocessing_comparison_fig = plot_model_comparison(preprocessing_results)
    preprocessing_comparison_fig.savefig('output/preprocessing_comparison.png')
    
    print(f"\nBest preprocessing approach: {best_approach} with R² = {best_r2:.4f}")
    
    # Now, evaluate different models with the best preprocessing approach
    print("\nEvaluating multiple regression models with the best preprocessing...")
    X_train_best, X_test_best, _ = best_approach_data
    
    models = {
        'Linear Regression': model_factory.get_model('linear_regression'),
        'Ridge': model_factory.get_model('ridge'),
        'Lasso': model_factory.get_model('lasso'),
        'ElasticNet': model_factory.get_model('elastic_net'),
        'SVR': model_factory.get_model('svr'),
        'Random Forest': model_factory.get_model('random_forest')
    }
    
    results, predictions, trained_models = evaluate_multiple_models(
        models, X_train_best, y_train, X_test_best, y_test
    )
    
    # Print model results
    for name, metrics in results.items():
        print(f"{name}: R² = {metrics['r2']:.4f}, RMSE = {metrics['rmse']:.4f}")
    
    # Plot model comparison
    model_comparison_fig = plot_model_comparison(results)
    model_comparison_fig.savefig('output/model_comparison.png')
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
    best_model = trained_models[best_model_name]
    best_model_pred = predictions[best_model_name]
    
    print(f"\nBest model: {best_model_name} with R² = {results[best_model_name]['r2']:.4f}")
    
    # Plot actual vs predicted for best model
    plot_actual_vs_predicted(y_test, best_model_pred, best_model_name).savefig(
        'output/actual_vs_predicted.png'
    )
    
    # Plot residuals for best model
    plot_residuals(y_test, best_model_pred, best_model_name).savefig(
        'output/residuals.png'
    )
    
    # Try to plot feature importance for best model
    try:
        plot_feature_importance(best_model, feature_names, best_model_name).savefig(
            'output/feature_importance.png'
        )
    except:
        print("Could not generate feature importance plot for this model type")
    
    print("\nAnalysis complete. Results and visualizations saved to 'output' directory.")
    

if __name__ == "__main__":
    main()
