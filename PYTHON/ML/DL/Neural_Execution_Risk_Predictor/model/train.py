"""
Training script for Neural Execution Risk Predictor
Can be run standalone or imported into notebooks
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Set random seeds
np.random.seed(42)
tf.random.set_seed(42)


def load_data(data_path):
    """Load combined dataset"""
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples")
    return df


def preprocess_data(df, test_size=0.15, val_size=0.176):
    """
    Preprocess data: split and scale
    
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test, scaler)
    """
    # Separate features and labels
    X = df.drop(columns=['failure_label']).values
    y = df['failure_label'].values
    
    # Split data
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=42, stratify=y_temp
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert labels to categorical
    y_train_cat = keras.utils.to_categorical(y_train, num_classes=3)
    y_val_cat = keras.utils.to_categorical(y_val, num_classes=3)
    y_test_cat = keras.utils.to_categorical(y_test, num_classes=3)
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    return (X_train_scaled, X_val_scaled, X_test_scaled,
            y_train_cat, y_val_cat, y_test_cat,
            y_train, y_val, y_test, scaler)


def build_model(input_dim=9):
    """Build neural network model"""
    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(64, activation='relu', name='hidden_layer_1'),
        layers.Dropout(0.2, name='dropout'),
        layers.Dense(32, activation='relu', name='hidden_layer_2'),
        layers.Dense(3, activation='softmax', name='output_layer')
    ], name='NeuralExecutionRiskPredictor')
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def train_model(model, X_train, y_train, X_val, y_val):
    """Train the model"""
    early_stopping = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=1
    )
    
    return history


def evaluate_model(model, X_test, y_test_cat, y_test_original):
    """Evaluate model performance"""
    # Get predictions
    test_loss, test_accuracy = model.evaluate(X_test, y_test_cat, verbose=0)
    y_pred_probs = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Calculate metrics
    precision = precision_score(y_test_original, y_pred, average=None)
    recall = recall_score(y_test_original, y_pred, average=None)
    cm = confusion_matrix(y_test_original, y_pred)
    
    results = {
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'precision': precision.tolist(),
        'recall': recall.tolist(),
        'confusion_matrix': cm.tolist()
    }
    
    return results, y_pred


def save_model_artifacts(model, scaler, results, model_dir):
    """Save model, scaler, and metadata"""
    os.makedirs(model_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(model_dir, 'risk_model.h5')
    model.save(model_path)
    print(f"Model saved to: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(model_dir, 'scaler.joblib')
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to: {scaler_path}")
    
    # Save metadata
    feature_names = [
        'num_steps', 'num_tools', 'tool_diversity',
        'has_high_risk_tool', 'est_tokens', 'max_retries',
        'sequential_tool_calls', 'plan_depth', 'time_limit_sec'
    ]
    
    metadata = {
        'model_name': 'Neural Execution Risk Predictor',
        'version': '1.0',
        'input_features': feature_names,
        'output_classes': {0: 'LOW_RISK', 1: 'MEDIUM_RISK', 2: 'HIGH_RISK'},
        'architecture': {
            'layers': ['Dense(64, ReLU)', 'Dropout(0.2)', 'Dense(32, ReLU)', 'Dense(3, Softmax)'],
            'optimizer': 'Adam',
            'learning_rate': 0.001,
            'loss': 'categorical_crossentropy'
        },
        'performance': results
    }
    
    metadata_path = os.path.join(model_dir, 'model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to: {metadata_path}")


def main():
    """Main training pipeline"""
    # Paths
    PROJECT_ROOT = r"D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor"
    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "execution_risk_dataset.csv")
    MODEL_DIR = os.path.join(PROJECT_ROOT, "model")
    
    print("="*60)
    print("Neural Execution Risk Predictor - Training Pipeline")
    print("="*60)
    
    # Load data
    df = load_data(DATA_PATH)
    
    # Preprocess
    (X_train, X_val, X_test,
     y_train_cat, y_val_cat, y_test_cat,
     y_train_orig, y_val_orig, y_test_orig,
     scaler) = preprocess_data(df)
    
    # Build model
    print("\nBuilding model...")
    model = build_model(input_dim=X_train.shape[1])
    model.summary()
    
    # Train
    print("\nTraining model...")
    history = train_model(model, X_train, y_train_cat, X_val, y_val_cat)
    
    # Evaluate
    print("\nEvaluating model...")
    results, y_pred = evaluate_model(model, X_test, y_test_cat, y_test_orig)
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    print(f"Test Loss: {results['test_loss']:.4f}")
    print(f"Precision per class: {results['precision']}")
    print(f"Recall per class: {results['recall']}")
    
    # Save artifacts
    print("\nSaving model artifacts...")
    save_model_artifacts(model, scaler, results, MODEL_DIR)
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    
    return model, scaler, results


if __name__ == "__main__":
    main()
