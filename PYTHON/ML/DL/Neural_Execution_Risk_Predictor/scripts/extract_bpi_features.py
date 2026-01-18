"""
BPI Challenge 2012 Feature Extraction Script
Extracts execution trace features from XES event logs
"""
import pm4py
import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


def extract_case_features(case_events):
    """
    Extract features from a single case (execution trace)
    
    Args:
        case_events: DataFrame of events for a single case
        
    Returns:
        dict: Features for this case
    """
    # Basic metrics
    num_steps = len(case_events)
    
    # Activity diversity (unique activities = tool diversity)
    activities = case_events['concept:name'].tolist()
    num_tools = len(set(activities))
    tool_diversity = num_tools
    
    # Detect sequential tool calls (repeated activities)
    sequential_calls = 0
    for i in range(len(activities) - 1):
        if activities[i] == activities[i + 1]:
            sequential_calls += 1
    
    # Estimate plan depth (based on activity patterns)
    # Higher depth means more nested/complex execution
    activity_counts = Counter(activities)
    max_repetition = max(activity_counts.values()) if activity_counts else 1
    plan_depth = min(max_repetition, 5)  # Cap at 5
    
    # Estimate tokens (proxy: num_steps * avg_activity_complexity)
    # More steps and diverse activities = more tokens
    est_tokens = num_steps * 200 + tool_diversity * 500
    
    # Time metrics
    if 'time:timestamp' in case_events.columns:
        time_diff = (case_events['time:timestamp'].max() - 
                    case_events['time:timestamp'].min())
        time_limit_sec = int(time_diff.total_seconds()) if hasattr(time_diff, 'total_seconds') else 300
    else:
        time_limit_sec = 300  # Default
    
    # High-risk tool detection (certain activities are risky)
    high_risk_activities = [
        'W_Completeren aanvraag',  # Complex completion tasks
        'W_Nabellen offertes',     # External calls
        'W_Valideren aanvraag'     # Validation tasks
    ]
    has_high_risk_tool = any(act in high_risk_activities for act in activities)
    
    # Max retries (estimate from repeated activities)
    max_retries = min(sequential_calls, 5)
    
    return {
        'num_steps': num_steps,
        'num_tools': num_tools,
        'tool_diversity': tool_diversity,
        'has_high_risk_tool': int(has_high_risk_tool),
        'est_tokens': est_tokens,
        'max_retries': max_retries,
        'sequential_tool_calls': sequential_calls,
        'plan_depth': plan_depth,
        'time_limit_sec': time_limit_sec
    }


def assign_risk_label(features):
    """
    Assign risk label based on engineering rules
    
    Rules:
    - HIGH_RISK (2): num_steps > 12 OR est_tokens > 9000 OR sequential_tool_calls > 8
    - MEDIUM_RISK (1): num_steps > 6 OR est_tokens > 5000 OR sequential_tool_calls > 4
    - LOW_RISK (0): Otherwise
    """
    if (features['num_steps'] > 12 or 
        features['est_tokens'] > 9000 or 
        features['sequential_tool_calls'] > 8 or
        (features['has_high_risk_tool'] == 1 and features['num_steps'] > 10)):
        return 2  # HIGH_RISK
    elif (features['num_steps'] > 6 or 
          features['est_tokens'] > 5000 or 
          features['sequential_tool_calls'] > 4):
        return 1  # MEDIUM_RISK
    else:
        return 0  # LOW_RISK


def extract_bpi_features(xes_file_path, output_csv_path):
    """
    Extract features from BPI Challenge 2012 XES file
    
    Args:
        xes_file_path: Path to the XES file
        output_csv_path: Path to save the extracted features CSV
    """
    print(f"Loading XES file: {xes_file_path}")
    
    # Load XES file using pm4py
    log = pm4py.read_xes(xes_file_path)
    
    print(f"Loaded {len(log)} cases from XES file")
    
    # Convert to DataFrame for easier processing
    df = pm4py.convert_to_dataframe(log)
    
    print("Extracting features from cases...")
    
    # Extract features for each case
    features_list = []
    case_ids = df['case:concept:name'].unique()
    
    for i, case_id in enumerate(case_ids):
        if i % 500 == 0:
            print(f"Processing case {i}/{len(case_ids)}")
        
        case_events = df[df['case:concept:name'] == case_id]
        features = extract_case_features(case_events)
        features['case_id'] = case_id
        features_list.append(features)
    
    # Create DataFrame
    features_df = pd.DataFrame(features_list)
    
    # Assign risk labels
    print("Assigning risk labels...")
    features_df['failure_label'] = features_df.apply(assign_risk_label, axis=1)
    
    # Reorder columns
    columns_order = [
        'case_id',
        'num_steps',
        'num_tools',
        'tool_diversity',
        'has_high_risk_tool',
        'est_tokens',
        'max_retries',
        'sequential_tool_calls',
        'plan_depth',
        'time_limit_sec',
        'failure_label'
    ]
    features_df = features_df[columns_order]
    
    # Save to CSV
    features_df.to_csv(output_csv_path, index=False)
    print(f"\nExtracted {len(features_df)} execution traces")
    print(f"Saved features to: {output_csv_path}")
    
    # Print label distribution
    print("\nRisk Label Distribution:")
    print(features_df['failure_label'].value_counts().sort_index())
    print("\nLabel Mapping:")
    print("  0 = LOW_RISK")
    print("  1 = MEDIUM_RISK")
    print("  2 = HIGH_RISK")
    
    return features_df


if __name__ == "__main__":
    # Paths
    xes_file = r"D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor\new_BPI_Challenge_2012.xes"
    output_csv = r"D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor\data\bpi_features.csv"
    
    # Extract features
    df = extract_bpi_features(xes_file, output_csv)
    
    # Print summary statistics
    print("\n" + "="*60)
    print("FEATURE SUMMARY STATISTICS")
    print("="*60)
    print(df.describe())
