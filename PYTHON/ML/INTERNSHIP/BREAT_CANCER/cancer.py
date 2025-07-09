# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.datasets import load_breast_cancer
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc

# # Load the breast cancer dataset
# print("Loading Breast Cancer dataset...")
# data = load_breast_cancer()
# X = data.data
# y = data.target

# # Create a DataFrame for better handling (optional but helpful)
# feature_names = data.feature_names
# df = pd.DataFrame(X, columns=feature_names)
# df['target'] = y

# print(f"Dataset shape: {df.shape}")
# print(f"Feature names: {feature_names}")
# print(f"Target names: {data.target_names}")
# print(f"Class distribution: {pd.Series(y).value_counts()}")

# # Note: The Breast Cancer dataset doesn't have categorical features that need one-hot encoding
# # But I'll show how you would handle them if they existed

# # Let's split the data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
# print(f"Training set shape: {X_train.shape}")
# print(f"Test set shape: {X_test.shape}")

# # Example of creating a pipeline with preprocessing (including one-hot encoding if needed)
# # For demonstration, let's pretend the first feature is categorical
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', StandardScaler(), slice(1, X.shape[1])),  # Scale all features except the first one
#         ('cat', OneHotEncoder(), [0])  # Apply one-hot encoding to the first feature (for demonstration)
#     ])

# # Create a pipeline with preprocessing and logistic regression
# pipeline = Pipeline([
#     ('preprocessor', preprocessor),
#     ('classifier', LogisticRegression(max_iter=1000, random_state=42))
# ])

# # Train the model
# print("Training the logistic regression model...")
# pipeline.fit(X_train, y_train)

# # Make predictions
# y_pred = pipeline.predict(X_test)
# y_prob = pipeline.predict_proba(X_test)[:, 1]

# # Evaluate the model
# print("\nModel Evaluation:")
# print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred, target_names=data.target_names))

# # Display confusion matrix
# cm = confusion_matrix(y_test, y_pred)
# print("\nConfusion Matrix:")
# print(cm)

# # Calculate ROC curve and AUC
# fpr, tpr, _ = roc_curve(y_test, y_prob)
# roc_auc = auc(fpr, tpr)

# # Plot ROC curve
# plt.figure(figsize=(8, 6))
# plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
# plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver Operating Characteristic (ROC) Curve')
# plt.legend(loc="lower right")
# plt.show()

# # Get feature importance (coefficients)
# if hasattr(pipeline.named_steps['classifier'], 'coef_'):
#     # Get the feature names after preprocessing (including one-hot encoded features)
#     # Note: This is simplified; you would need to handle the actual feature names
#     # from your preprocessing pipeline if it transforms them
#     coefficients = pipeline.named_steps['classifier'].coef_[0]
    
#     # Create a DataFrame of features and their importance
#     coef_df = pd.DataFrame({
#         'Feature': feature_names,
#         'Coefficient': coefficients[-len(feature_names):]  # Adjust based on actual preprocessing
#     })
    
#     # Sort by absolute coefficient values
#     coef_df = coef_df.reindex(coef_df['Coefficient'].abs().sort_values(ascending=False).index)
    
#     print("\nTop 10 Most Important Features:")
#     print(coef_df.head(10))

# print("\nTraining and evaluation complete!")


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.datasets import load_breast_cancer
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc

# # Load the breast cancer dataset
# print("Loading Breast Cancer dataset...")
# data = load_breast_cancer()
# X = data.data
# y = data.target
# feature_names = data.feature_names

# # Create a DataFrame for better handling
# df = pd.DataFrame(X, columns=feature_names)
# df['target'] = y

# print(f"Dataset shape: {df.shape}")
# print(f"Feature names: {feature_names}")
# print(f"Target names: {data.target_names}")
# print(f"Class distribution: {pd.Series(y).value_counts()}")

# # Create a categorical feature by binning the first feature (mean radius)
# print("\nCreating a categorical feature from 'mean radius'...")
# # Bin the first feature into 3 categories
# df['radius_category'] = pd.cut(df['mean radius'], bins=3, labels=['small', 'medium', 'large'])
# print(f"Radius categories distribution:\n{df['radius_category'].value_counts()}")

# # Split data into train and test sets
# X = df.drop(['target', 'radius_category', 'mean radius'], axis=1)  # Remove target and categorical source
# y = df['target']
# categorical_feature = pd.get_dummies(df['radius_category'], prefix='radius')  # Manual one-hot encoding

# # Combine the one-hot encoded features with the original numerical features
# X = pd.concat([X, categorical_feature], axis=1)
# print(f"Features after one-hot encoding: {X.shape[1]}")

# # Split the data
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.25, random_state=42, stratify=y
# )
# print(f"Training set shape: {X_train.shape}")
# print(f"Test set shape: {X_test.shape}")

# # Standardize the numerical features (excluding one-hot encoded columns)
# numerical_cols = list(X.columns[:-3])  # All except the one-hot encoded columns
# scaler = StandardScaler()
# X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
# X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

# # Train logistic regression model
# print("\nTraining the logistic regression model...")
# model = LogisticRegression(max_iter=1000, random_state=42)
# model.fit(X_train, y_train)

# # Make predictions
# y_pred = model.predict(X_test)
# y_prob = model.predict_proba(X_test)[:, 1]

# # Evaluate the model
# print("\nModel Evaluation:")
# print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred, target_names=data.target_names))

# # Display confusion matrix
# cm = confusion_matrix(y_test, y_pred)
# print("\nConfusion Matrix:")
# print(cm)

# # Calculate ROC curve and AUC
# fpr, tpr, _ = roc_curve(y_test, y_prob)
# roc_auc = auc(fpr, tpr)

# # Plot ROC curve
# plt.figure(figsize=(8, 6))
# plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
# plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver Operating Characteristic (ROC) Curve')
# plt.legend(loc="lower right")
# plt.show()

# # Get feature importance (coefficients)
# if hasattr(model, 'coef_'):
#     # Get all feature names including one-hot encoded ones
#     all_feature_names = list(X.columns)
#     coefficients = model.coef_[0]
    
#     # Create a DataFrame of features and their importance
#     coef_df = pd.DataFrame({
#         'Feature': all_feature_names,
#         'Coefficient': coefficients
#     })
    
#     # Sort by absolute coefficient values
#     coef_df = coef_df.sort_values(by='Coefficient', key=abs, ascending=False)
    
#     print("\nTop 10 Most Important Features:")
#     print(coef_df.head(10))
    
#     # See how the radius categories compare
#     print("\nCoefficients for radius categories:")
#     radius_coefs = coef_df[coef_df['Feature'].str.contains('radius_')]
#     print(radius_coefs)

# print("\nTraining and evaluation complete!")

# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, average_precision_score
)

# Set display options and style for better visualization
pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set(font_scale=1.2)

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Load the breast cancer dataset
print("Loading Breast Cancer dataset...")
data = load_breast_cancer()
X = data.data
y = data.target
feature_names = data.feature_names

# Create a DataFrame for better handling
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Display basic dataset information
print(f"Dataset shape: {df.shape}")
print(f"Target names: {data.target_names}")
print(f"Class distribution:\n{pd.Series(y).value_counts()}")

# Create a categorical feature by binning 'mean radius'
print("\nCreating a categorical feature from 'mean radius'...")
df['radius_category'] = pd.cut(df['mean radius'], bins=3, labels=['small', 'medium', 'large'])
print(f"Radius categories distribution:\n{df['radius_category'].value_counts()}")

# Visualize the radius categories
plt.figure(figsize=(10, 5))
sns.countplot(x='radius_category', hue='target', data=df, palette='viridis')
plt.title('Radius Categories by Target Class')
plt.xlabel('Radius Category')
plt.ylabel('Count')
plt.legend(title='Target', labels=data.target_names)
plt.show()

# Prepare features for modeling
X = df.drop(['target', 'radius_category', 'mean radius'], axis=1)
y = df['target']
categorical_feature = pd.get_dummies(df['radius_category'], prefix='radius')

# Combine numerical and one-hot encoded features
X = pd.concat([X, categorical_feature], axis=1)
print(f"Features after one-hot encoding: {X.shape[1]}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print(f"Training set shape: {X_train.shape}")
print(f"Test set shape: {X_test.shape}")

# Standardize numerical features
numerical_cols = list(X.columns[:-3])  # All except one-hot encoded columns
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

# Train logistic regression model
print("\nTraining the logistic regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# ----------------- EVALUATION METRICS -----------------

# 1. Basic classification metrics
print("\n--- CLASSIFICATION METRICS ---")
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

metrics_df = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    'Value': [accuracy, precision, recall, f1]
})
print(metrics_df)

# 2. Classification report
print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_test, y_pred, target_names=data.target_names))

# 3. Confusion matrix
print("\n--- CONFUSION MATRIX ---")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# 4. Confusion matrix visualization
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=data.target_names,
            yticklabels=data.target_names)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# 5. ROC curve and AUC
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.grid(True)
plt.show()

# 6. Precision-Recall curve
precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_prob)
average_precision = average_precision_score(y_test, y_prob)

plt.figure(figsize=(10, 8))
plt.step(recall_curve, precision_curve, color='b', alpha=0.2, where='post')
plt.fill_between(recall_curve, precision_curve, step='post', alpha=0.2, color='b')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title(f'Precision-Recall Curve: AP={average_precision:.3f}')
plt.grid(True)
plt.show()

# 7. Feature importance
if hasattr(model, 'coef_'):
    # Get all feature names including one-hot encoded ones
    all_feature_names = list(X.columns)
    coefficients = model.coef_[0]
    
    # Create a DataFrame of features and their importance
    coef_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': coefficients
    })
    
    # Sort by absolute coefficient values
    coef_df = coef_df.sort_values(by='Coefficient', key=abs, ascending=False)
    
    print("\n--- TOP 10 MOST IMPORTANT FEATURES ---")
    print(coef_df.head(10))
    
    # Plot top 15 features
    plt.figure(figsize=(12, 10))
    top_features = coef_df.head(15)
    colors = ['red' if x < 0 else 'green' for x in top_features['Coefficient']]
    
    sns.barplot(x='Coefficient', y='Feature', data=top_features, palette=colors)
    plt.title('Top 15 Features by Importance')
    plt.axvline(x=0, color='black', linestyle='-')
    plt.tight_layout()
    plt.show()
    
    # See how the radius categories compare
    print("\n--- COEFFICIENTS FOR RADIUS CATEGORIES ---")
    radius_coefs = coef_df[coef_df['Feature'].str.contains('radius_')]
    print(radius_coefs)

# 8. Cross-validation for more robust metrics
print("\n--- CROSS-VALIDATION RESULTS (5-FOLD) ---")
cv_accuracy = cross_val_score(LogisticRegression(max_iter=1000, random_state=42), 
                             X, y, cv=5, scoring='accuracy')
cv_precision = cross_val_score(LogisticRegression(max_iter=1000, random_state=42), 
                              X, y, cv=5, scoring='precision')
cv_recall = cross_val_score(LogisticRegression(max_iter=1000, random_state=42), 
                           X, y, cv=5, scoring='recall')
cv_f1 = cross_val_score(LogisticRegression(max_iter=1000, random_state=42), 
                        X, y, cv=5, scoring='f1')

print(f"Accuracy: {cv_accuracy.mean():.4f} ± {cv_accuracy.std():.4f}")
print(f"Precision: {cv_precision.mean():.4f} ± {cv_precision.std():.4f}")
print(f"Recall: {cv_recall.mean():.4f} ± {cv_recall.std():.4f}")
print(f"F1 Score: {cv_f1.mean():.4f} ± {cv_f1.std():.4f}")

# 9. Feature distribution visualization
features_to_plot = coef_df.head(3)['Feature'].values  # Top 3 most important features

plt.figure(figsize=(15, 5))
for i, feature in enumerate(features_to_plot):
    if feature in df.columns:  # Only plot if feature is in original dataframe
        plt.subplot(1, 3, i+1)
        for target_val in [0, 1]:
            sns.kdeplot(
                df[df['target'] == target_val][feature],
                label=f"{data.target_names[target_val]}"
            )
        plt.title(f'Distribution of {feature}')
        plt.xlabel(feature)
        plt.legend()
plt.tight_layout()
plt.show()

print("\nAnalysis complete!")