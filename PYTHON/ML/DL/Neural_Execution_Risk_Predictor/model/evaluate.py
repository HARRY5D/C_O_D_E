"""
Evaluation script for Neural Execution Risk Predictor
Generates detailed evaluation reports and visualizations
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

import tensorflow as tf
from tensorflow import keras

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    confusion_matrix, classification_report
)
from sklearn.inspection import permutation_importance


class KerasClassifierWrapper:
    """Wrapper for permutation importance"""
    def __init__(self, model):
        self.model = model
    
    def predict(self, X):
        probs = self.model.predict(X, verbose=0)
        return np.argmax(probs, axis=1)
    
    def score(self, X, y):
        y_pred = self.predict(X)
        return accuracy_score(y, y_pred)


def evaluate_model(model_path, scaler_path, test_data_path, reports_dir):
    """
    Comprehensive model evaluation
    
    Args:
        model_path: Path to saved model (.h5)
        scaler_path: Path to saved scaler (.joblib)
        test_data_path: Path to test dataset (.csv)
        reports_dir: Directory to save evaluation reports
    """
    print("="*60)
    print("Neural Execution Risk Predictor - Evaluation")
    print("="*60)
    
    # Create reports directory
    os.makedirs(reports_dir, exist_ok=True)
    
    # Load model and scaler
    print("\nLoading model and scaler...")
    model = keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    
    # Load test data
    print("Loading test data...")
    df_test = pd.read_csv(test_data_path)
    
    X_test = df_test.drop(columns=['failure_label']).values
    y_test = df_test['failure_label'].values
    
    # Scale features
    X_test_scaled = scaler.transform(X_test)
    
    # Make predictions
    print("Making predictions...")
    y_pred_probs = model.predict(X_test_scaled, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Calculate metrics
    print("\n" + "="*60)
    print("PERFORMANCE METRICS")
    print("="*60)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average=None)
    recall = recall_score(y_test, y_pred, average=None)
    
    print(f"\nOverall Accuracy: {accuracy:.4f}")
    print(f"\nPer-Class Metrics:")
    print(f"  LOW_RISK    - Precision: {precision[0]:.4f}, Recall: {recall[0]:.4f}")
    print(f"  MEDIUM_RISK - Precision: {precision[1]:.4f}, Recall: {recall[1]:.4f}")
    print(f"  HIGH_RISK   - Precision: {precision[2]:.4f}, Recall: {recall[2]:.4f}")
    
    # Classification report
    print("\n" + "="*60)
    print("DETAILED CLASSIFICATION REPORT")
    print("="*60)
    target_names = ['LOW_RISK', 'MEDIUM_RISK', 'HIGH_RISK']
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['LOW', 'MEDIUM', 'HIGH'],
                yticklabels=['LOW', 'MEDIUM', 'HIGH'])
    plt.xlabel('Predicted', fontsize=12, fontweight='bold')
    plt.ylabel('Actual', fontsize=12, fontweight='bold')
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    cm_path = os.path.join(reports_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix saved to: {cm_path}")
    plt.close()
    
    # Feature importance
    print("\n" + "="*60)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("="*60)
    
    feature_names = [
        'num_steps', 'num_tools', 'tool_diversity',
        'has_high_risk_tool', 'est_tokens', 'max_retries',
        'sequential_tool_calls', 'plan_depth', 'time_limit_sec'
    ]
    
    wrapped_model = KerasClassifierWrapper(model)
    
    print("Calculating permutation importance...")
    perm_importance = permutation_importance(
        wrapped_model, X_test_scaled, y_test,
        n_repeats=10, random_state=42, n_jobs=-1
    )
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': perm_importance.importances_mean,
        'Std': perm_importance.importances_std
    }).sort_values('Importance', ascending=False)
    
    print("\nFeature Importance:")
    print(importance_df.to_string(index=False))
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'],
             xerr=importance_df['Std'], capsize=5, color='steelblue', alpha=0.8)
    plt.xlabel('Importance (Drop in Accuracy)', fontsize=12, fontweight='bold')
    plt.ylabel('Feature', fontsize=12, fontweight='bold')
    plt.title('Feature Importance', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    fi_path = os.path.join(reports_dir, 'feature_importance.png')
    plt.savefig(fi_path, dpi=300, bbox_inches='tight')
    print(f"Feature importance plot saved to: {fi_path}")
    plt.close()
    
    # Error analysis
    print("\n" + "="*60)
    print("ERROR ANALYSIS")
    print("="*60)
    
    false_positives = {
        'LOW→MEDIUM': cm[0, 1],
        'LOW→HIGH': cm[0, 2],
        'MEDIUM→HIGH': cm[1, 2]
    }
    
    false_negatives = {
        'MEDIUM→LOW': cm[1, 0],
        'HIGH→LOW': cm[2, 0],
        'HIGH→MEDIUM': cm[2, 1]
    }
    
    print("\nFalse Positives (over-estimation):")
    for transition, count in false_positives.items():
        print(f"  {transition}: {count}")
    
    print("\nFalse Negatives (under-estimation):")
    for transition, count in false_negatives.items():
        print(f"  {transition}: {count}")
    
    # Critical error rate
    critical_errors = cm[2, 0] + cm[2, 1]
    total_high_risk = cm[2, :].sum()
    if total_high_risk > 0:
        critical_error_rate = critical_errors / total_high_risk
        print(f"\nCRITICAL ERROR RATE (missed HIGH_RISK): {critical_error_rate:.2%}")
    
    print("\n" + "="*60)
    print("Evaluation Complete!")
    print("="*60)
    
    return {
        'accuracy': accuracy,
        'precision': precision.tolist(),
        'recall': recall.tolist(),
        'confusion_matrix': cm.tolist(),
        'feature_importance': importance_df.to_dict('records')
    }


if __name__ == "__main__":
    # Paths
    PROJECT_ROOT = r"D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor"
    MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "risk_model.h5")
    SCALER_PATH = os.path.join(PROJECT_ROOT, "model", "scaler.joblib")
    TEST_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "execution_risk_dataset.csv")
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    
    results = evaluate_model(MODEL_PATH, SCALER_PATH, TEST_DATA_PATH, REPORTS_DIR)
