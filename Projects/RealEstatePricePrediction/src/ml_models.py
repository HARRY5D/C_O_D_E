"""
Machine Learning Models Module for Real Estate Price Prediction
Implements multiple ML algorithms with hyperparameter tuning and evaluation
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
import xgboost as xgb
import lightgbm as lgb
try:
    import catboost as cb
except ImportError:
    cb = None

import joblib
import warnings
warnings.filterwarnings('ignore')

class MLModelManager:
    def __init__(self):
        self.models = {}
        self.trained_models = {}
        self.best_model = None
        self.model_performance = {}
        
    def initialize_models(self):
        """Initialize all available models"""
        self.models = {
            'linear_regression': LinearRegression(),
            'ridge': Ridge(alpha=1.0),
            'lasso': Lasso(alpha=1.0),
            'decision_tree': DecisionTreeRegressor(random_state=42),
            'random_forest': RandomForestRegressor(
                n_estimators=100, 
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                random_state=42
            ),
            'xgboost': xgb.XGBRegressor(
                n_estimators=100,
                random_state=42,
                eval_metric='rmse'
            ),
            'lightgbm': lgb.LGBMRegressor(
                n_estimators=100,
                random_state=42,
                verbose=-1
            )
        }
        
        # Add CatBoost if available
        if cb is not None:
            self.models['catboost'] = cb.CatBoostRegressor(
                iterations=100,
                random_state=42,
                verbose=False
            )
        
        print(f"Initialized {len(self.models)} models: {list(self.models.keys())}")
    
    def train_model(self, model_name: str, X_train: pd.DataFrame, y_train: pd.Series):
        """Train a specific model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found. Available models: {list(self.models.keys())}")
        
        print(f"Training {model_name}...")
        model = self.models[model_name]
        model.fit(X_train, y_train)
        self.trained_models[model_name] = model
        print(f"{model_name} training completed.")
        
        return model
    
    def train_all_models(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train all available models"""
        print("Training all models...")
        
        for model_name in self.models.keys():
            try:
                self.train_model(model_name, X_train, y_train)
            except Exception as e:
                print(f"Error training {model_name}: {e}")
        
        print(f"Training completed for {len(self.trained_models)} models.")
    
    def evaluate_model(self, model_name: str, X_test: pd.DataFrame, y_test: pd.Series):
        """Evaluate a trained model"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not trained yet.")
        
        model = self.trained_models[model_name]
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        metrics = {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'MAPE': mape
        }
        
        self.model_performance[model_name] = metrics
        return metrics, y_pred
    
    def evaluate_all_models(self, X_test: pd.DataFrame, y_test: pd.Series):
        """Evaluate all trained models"""
        print("Evaluating all models...")
        
        results = {}
        predictions = {}
        
        for model_name in self.trained_models.keys():
            try:
                metrics, y_pred = self.evaluate_model(model_name, X_test, y_test)
                results[model_name] = metrics
                predictions[model_name] = y_pred
                print(f"{model_name} - R2: {metrics['R2']:.4f}, RMSE: {metrics['RMSE']:.2f}")        except Exception as e:
                print(f"Error evaluating {model_name}: {e}")
        
        return results, predictions
    
    def get_model_comparison(self):
        """Get comparison of all model performances"""
        if not self.model_performance:
            print("No model performance data available. Please evaluate models first.")
            return None
        
        comparison_df = pd.DataFrame(self.model_performance).T
        comparison_df = comparison_df.sort_values('R2', ascending=False)
        
        return comparison_df
    
    def train_multiple_models(self, df: pd.DataFrame):
        """Train multiple models and return results"""
        print("🤖 Training multiple ML models...")
        
        # Initialize models
        self.initialize_models()
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col not in ['price', 'property_id', 'description']]
        X = df[feature_columns]
        y = df['price']
        
        # Handle categorical variables
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        for col in categorical_columns:
            X[col] = pd.Categorical(X[col]).codes
        
        # Fill any NaN values
        X = X.fillna(X.mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train all models
        self.train_all_models(X_train, y_train)
        
        # Evaluate all models
        results, predictions = self.evaluate_all_models(X_test, y_test)
        
        return results
    
    def select_best_model(self, metric='R2'):
        """Select the best performing model"""
        if not self.model_performance:
            print("No model performance data available.")
            return None
        
        if metric in ['MSE', 'RMSE', 'MAE', 'MAPE']:
            best_model_name = min(self.model_performance.keys(), 
                                key=lambda x: self.model_performance[x][metric])
        else:  # R2
            best_model_name = max(self.model_performance.keys(), 
                                key=lambda x: self.model_performance[x][metric])
        
        self.best_model = {
            'name': best_model_name,
            'model': self.trained_models[best_model_name],
            'performance': self.model_performance[best_model_name]
        }
        
        print(f"Best model selected: {best_model_name} with {metric}: {self.model_performance[best_model_name][metric]:.4f}")
        return self.best_model
    
    def cross_validate_model(self, model_name: str, X: pd.DataFrame, y: pd.Series, cv=5):
        """Perform cross-validation for a model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found.")
        
        model = self.models[model_name]
        
        # Perform cross-validation
        cv_scores = cross_val_score(model, X, y, cv=cv, 
                                  scoring='neg_mean_squared_error', n_jobs=-1)
        cv_rmse_scores = np.sqrt(-cv_scores)
        
        cv_results = {
            'mean_rmse': cv_rmse_scores.mean(),
            'std_rmse': cv_rmse_scores.std(),
            'scores': cv_rmse_scores
        }
        
        print(f"{model_name} CV Results - RMSE: {cv_results['mean_rmse']:.2f} (+/- {cv_results['std_rmse']:.2f})")
        return cv_results
    
    def hyperparameter_tuning(self, model_name: str, X_train: pd.DataFrame, y_train: pd.Series):
        """Perform hyperparameter tuning for specific models"""
        param_grids = {
            'random_forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10]
            },
            'xgboost': {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2]
            },
            'lightgbm': {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2]
            }
        }
        
        if model_name not in param_grids:
            print(f"Hyperparameter tuning not available for {model_name}")
            return None
        
        print(f"Performing hyperparameter tuning for {model_name}...")
        
        model = self.models[model_name]
        param_grid = param_grids[model_name]
        
        grid_search = GridSearchCV(
            model, param_grid, cv=3, 
            scoring='neg_mean_squared_error', 
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        # Update the model with best parameters
        self.models[model_name] = grid_search.best_estimator_
        
        print(f"Best parameters for {model_name}: {grid_search.best_params_}")
        print(f"Best CV score: {np.sqrt(-grid_search.best_score_):.2f}")
        
        return grid_search.best_params_
    
    def get_feature_importance(self, model_name: str, feature_names: list):
        """Get feature importance from tree-based models"""
        if model_name not in self.trained_models:
            print(f"Model {model_name} not trained yet.")
            return None
        
        model = self.trained_models[model_name]
        
        # Check if model has feature_importances_ attribute
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return importance_df
        else:
            print(f"Model {model_name} does not support feature importance.")
            return None
    
    def predict_single_property(self, property_features: dict, model_name: str = None):
        """Predict price for a single property"""
        if model_name is None:
            if self.best_model is None:
                self.select_best_model()
            model = self.best_model['model']
            model_name = self.best_model['name']
        else:
            if model_name not in self.trained_models:
                raise ValueError(f"Model {model_name} not trained yet.")
            model = self.trained_models[model_name]
        
        # Convert property features to DataFrame
        feature_df = pd.DataFrame([property_features])
        
        # Make prediction
        prediction = model.predict(feature_df)[0]
        
        # Get prediction interval (for tree-based models)
        confidence_interval = None
        if hasattr(model, 'estimators_'):
            predictions = np.array([tree.predict(feature_df)[0] for tree in model.estimators_])
            std = np.std(predictions)
            confidence_interval = (prediction - 1.96 * std, prediction + 1.96 * std)
        
        result = {
            'predicted_price': prediction,
            'model_used': model_name,
            'confidence_interval': confidence_interval
        }
        
        return result
    
    def save_model(self, model_name: str, filepath: str):
        """Save a trained model"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not trained yet.")
        
        joblib.dump(self.trained_models[model_name], filepath)
        print(f"Model {model_name} saved to {filepath}")
    
    def load_model(self, model_name: str, filepath: str):
        """Load a saved model"""
        try:
            model = joblib.load(filepath)
            self.trained_models[model_name] = model
            print(f"Model {model_name} loaded from {filepath}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def train_multiple_models(self, df: pd.DataFrame):
        """Train multiple models and return results"""
        print("🤖 Training multiple ML models...")
        
        # Initialize models
        self.initialize_models()
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col not in ['price', 'property_id', 'description']]
        X = df[feature_columns]
        y = df['price']
        
        # Handle categorical variables
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        for col in categorical_columns:
            X[col] = pd.Categorical(X[col]).codes
        
        # Fill any NaN values
        X = X.fillna(X.mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train all models
        self.train_all_models(X_train, y_train)
        
        # Evaluate all models
        results, predictions = self.evaluate_all_models(X_test, y_test)
        
        return results

class ModelExplainer:
    """Model explanation and interpretability tools"""
    
    def __init__(self, model, X_train, feature_names):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
    
    def explain_prediction(self, X_sample):
        """Explain individual prediction using SHAP values (if available)"""
        try:
            import shap
            
            # Create explainer
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(X_sample)
            
            # Create explanation DataFrame
            explanation_df = pd.DataFrame({
                'feature': self.feature_names,
                'feature_value': X_sample.iloc[0] if hasattr(X_sample, 'iloc') else X_sample[0],
                'shap_value': shap_values[0] if len(shap_values.shape) > 1 else shap_values
            })
            
            explanation_df['abs_shap_value'] = np.abs(explanation_df['shap_value'])
            explanation_df = explanation_df.sort_values('abs_shap_value', ascending=False)
            
            return explanation_df
            
        except ImportError:
            print("SHAP not available. Install with: pip install shap")
            return None
        except Exception as e:
            print(f"Error in SHAP explanation: {e}")
            return None
