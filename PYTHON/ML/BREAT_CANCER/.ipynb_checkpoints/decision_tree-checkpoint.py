# Complete Decision Tree Implementation for Breast Cancer Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("COMPLETE DECISION TREE vs LOGISTIC REGRESSION COMPARISON")
print("=" * 70)

# 1. LOAD AND PREPROCESS DATA
print("\n1. Loading and Preprocessing Data...")
data = load_breast_cancer()
X = data.data
y = data.target

# Create DataFrame
df = pd.DataFrame(X, columns=data.feature_names)
df['target'] = y

print(f"Dataset shape: {df.shape}")
print(f"Target distribution: {pd.Series(y).value_counts().to_dict()}")
print(f"Target names: {data.target_names}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training set shape: {X_train_scaled.shape}")
print(f"Test set shape: {X_test_scaled.shape}")

# 2. TRAIN MODELS
print("\n2. Training Models...")

# Train Decision Tree
dt_model = DecisionTreeClassifier(
    random_state=42, 
    max_depth=5,  # Prevent overfitting
    min_samples_split=10,
    min_samples_leaf=5
)
dt_model.fit(X_train_scaled, y_train)

# Train Logistic Regression for comparison
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_scaled, y_train)

print("✓ Decision Tree trained")
print("✓ Logistic Regression trained")

# 3. MAKE PREDICTIONS
dt_pred = dt_model.predict(X_test_scaled)
lr_pred = lr_model.predict(X_test_scaled)

# 4. EVALUATE MODELS
print("\n3. Model Evaluation...")

# Calculate metrics for both models
def calculate_metrics(y_true, y_pred, model_name):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    return {
        'Model': model_name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1_Score': f1
    }

dt_metrics = calculate_metrics(y_test, dt_pred, 'Decision Tree')
lr_metrics = calculate_metrics(y_test, lr_pred, 'Logistic Regression')

# Display metrics comparison
metrics_df = pd.DataFrame([dt_metrics, lr_metrics])
print("\nMODEL PERFORMANCE COMPARISON:")
print("-" * 50)
for metric in ['Accuracy', 'Precision', 'Recall', 'F1_Score']:
    print(f"{metric:<12} | DT: {dt_metrics[metric]:.4f} | LR: {lr_metrics[metric]:.4f}")

# 5. VISUALIZE DECISION TREE
print("\n4. Decision Tree Visualization...")

plt.figure(figsize=(20, 12))
plot_tree(dt_model, 
          feature_names=data.feature_names, 
          class_names=data.target_names,
          filled=True, 
          rounded=True, 
          fontsize=10)
plt.title("Decision Tree for Breast Cancer Classification", fontsize=16, pad=20)
plt.tight_layout()
plt.show()

# 6. FEATURE IMPORTANCE
print("\n5. Feature Importance Analysis...")

# Decision Tree feature importance
dt_importance = pd.DataFrame({
    'Feature': data.feature_names,
    'Importance': dt_model.feature_importances_
}).sort_values('Importance', ascending=False)

# Logistic Regression coefficients
lr_importance = pd.DataFrame({
    'Feature': data.feature_names,
    'Coefficient': abs(lr_model.coef_[0])
}).sort_values('Coefficient', ascending=False)

# Display top 10 features
print("\nTop 10 Most Important Features:")
print("\nDecision Tree:")
print(dt_importance.head(10).to_string(index=False))
print("\nLogistic Regression:")
print(lr_importance.head(10).to_string(index=False))

# Plot feature importance comparison
plt.figure(figsize=(15, 8))

plt.subplot(1, 2, 1)
top_dt = dt_importance.head(10)
plt.barh(range(len(top_dt)), top_dt['Importance'], color='lightblue')
plt.yticks(range(len(top_dt)), top_dt['Feature'])
plt.xlabel('Importance Score')
plt.title('Decision Tree Feature Importance')
plt.gca().invert_yaxis()

plt.subplot(1, 2, 2)
top_lr = lr_importance.head(10)
plt.barh(range(len(top_lr)), top_lr['Coefficient'], color='lightcoral')
plt.yticks(range(len(top_lr)), top_lr['Feature'])
plt.xlabel('Coefficient Magnitude')
plt.title('Logistic Regression Feature Importance')
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# 7. CONFUSION MATRICES
print("\n6. Confusion Matrix Analysis...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Decision Tree confusion matrix
cm_dt = confusion_matrix(y_test, dt_pred)
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues',
            xticklabels=data.target_names, yticklabels=data.target_names,
            ax=axes[0])
axes[0].set_title('Decision Tree\nConfusion Matrix')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

# Logistic Regression confusion matrix
cm_lr = confusion_matrix(y_test, lr_pred)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues',
            xticklabels=data.target_names, yticklabels=data.target_names,
            ax=axes[1])
axes[1].set_title('Logistic Regression\nConfusion Matrix')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

plt.tight_layout()
plt.show()

# 8. DECISION RULES EXTRACTION
print("\n7. Decision Tree Rules (First 15 lines)...")
tree_rules = export_text(dt_model, feature_names=list(data.feature_names))
rules_lines = tree_rules.split('\n')[:15]
for line in rules_lines:
    print(line)

# 9. MODEL COMPARISON SUMMARY
print("\n" + "=" * 70)
print("FINAL COMPARISON SUMMARY")
print("=" * 70)

better_dt = dt_metrics['Accuracy'] > lr_metrics['Accuracy']
print(f"\n🏆 BEST PERFORMING MODEL: {'Decision Tree' if better_dt else 'Logistic Regression'}")

print(f"\n📊 PERFORMANCE DIFFERENCES:")
acc_diff = abs(dt_metrics['Accuracy'] - lr_metrics['Accuracy'])
print(f"   • Accuracy difference: {acc_diff:.4f}")

print(f"\n🔍 INTERPRETABILITY:")
print(f"   • Decision Tree: High (explicit rules)")
print(f"   • Logistic Regression: Medium (linear relationships)")

print(f"\n⚡ DECISION BOUNDARIES:")
print(f"   • Decision Tree: Rectangular (axis-parallel)")
print(f"   • Logistic Regression: Linear")

# Common important features
dt_top5 = set(dt_importance.head(5)['Feature'])
lr_top5 = set(lr_importance.head(5)['Feature'])
common_features = dt_top5.intersection(lr_top5)

print(f"\n🎯 COMMONLY IMPORTANT FEATURES:")
for feature in common_features:
    print(f"   • {feature}")

print(f"\n✅ RECOMMENDATIONS:")
if better_dt:
    print(f"   • Use Decision Tree for better accuracy ({dt_metrics['Accuracy']:.4f})")
    print(f"   • Decision Tree provides explicit decision rules")
    print(f"   • Good for explaining individual predictions")
else:
    print(f"   • Use Logistic Regression for better accuracy ({lr_metrics['Accuracy']:.4f})")
    print(f"   • Logistic Regression provides probability estimates")
    print(f"   • More stable with new data")

print(f"\n📈 DATASET INSIGHTS:")
print(f"   • Total samples: {len(y)}")
print(f"   • Features: {X.shape[1]}")
print(f"   • Malignant cases: {sum(y == 0)} ({sum(y == 0)/len(y)*100:.1f}%)")
print(f"   • Benign cases: {sum(y == 1)} ({sum(y == 1)/len(y)*100:.1f}%)")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)