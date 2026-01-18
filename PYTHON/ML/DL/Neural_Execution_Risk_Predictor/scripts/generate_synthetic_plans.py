"""
Synthetic Agent Execution Plan Generator
Generates synthetic execution plans with varied risk profiles
"""
import pandas as pd
import numpy as np
import random


def generate_synthetic_plan(plan_id, risk_profile='random'):
    """
    Generate a single synthetic execution plan
    
    Args:
        plan_id: Unique identifier for the plan
        risk_profile: 'low', 'medium', 'high', or 'random'
        
    Returns:
        dict: Feature dictionary for the plan
    """
    if risk_profile == 'random':
        risk_profile = random.choice(['low', 'medium', 'high'])
    
    if risk_profile == 'low':
        # Low risk: simple, short executions
        num_steps = random.randint(2, 6)
        num_tools = random.randint(1, 3)
        tool_diversity = num_tools
        has_high_risk_tool = 0
        est_tokens = random.randint(800, 4000)
        max_retries = random.randint(0, 2)
        sequential_tool_calls = random.randint(0, 2)
        plan_depth = random.randint(1, 2)
        time_limit_sec = random.randint(30, 120)
        failure_label = 0
        
    elif risk_profile == 'medium':
        # Medium risk: moderate complexity
        num_steps = random.randint(6, 12)
        num_tools = random.randint(3, 6)
        tool_diversity = num_tools
        has_high_risk_tool = random.choice([0, 1])
        est_tokens = random.randint(4000, 9000)
        max_retries = random.randint(2, 4)
        sequential_tool_calls = random.randint(3, 6)
        plan_depth = random.randint(2, 3)
        time_limit_sec = random.randint(120, 300)
        failure_label = 1
        
    else:  # high risk
        # High risk: complex, resource-intensive
        num_steps = random.randint(12, 25)
        num_tools = random.randint(5, 12)
        tool_diversity = num_tools
        has_high_risk_tool = 1
        est_tokens = random.randint(9000, 20000)
        max_retries = random.randint(4, 8)
        sequential_tool_calls = random.randint(8, 15)
        plan_depth = random.randint(3, 5)
        time_limit_sec = random.randint(300, 600)
        failure_label = 2
    
    return {
        'plan_id': plan_id,
        'num_steps': num_steps,
        'num_tools': num_tools,
        'tool_diversity': tool_diversity,
        'has_high_risk_tool': has_high_risk_tool,
        'est_tokens': est_tokens,
        'max_retries': max_retries,
        'sequential_tool_calls': sequential_tool_calls,
        'plan_depth': plan_depth,
        'time_limit_sec': time_limit_sec,
        'failure_label': failure_label
    }


def generate_synthetic_dataset(num_samples=1000, distribution=None):
    """
    Generate a synthetic dataset of execution plans
    
    Args:
        num_samples: Total number of samples to generate
        distribution: Dict with risk distribution (e.g., {'low': 0.4, 'medium': 0.4, 'high': 0.2})
                     If None, uses balanced distribution
        
    Returns:
        DataFrame: Synthetic execution plans
    """
    if distribution is None:
        # Balanced distribution
        distribution = {'low': 0.33, 'medium': 0.34, 'high': 0.33}
    
    # Calculate samples per category
    samples_per_category = {
        'low': int(num_samples * distribution['low']),
        'medium': int(num_samples * distribution['medium']),
        'high': int(num_samples * distribution['high'])
    }
    
    # Adjust for rounding
    total_assigned = sum(samples_per_category.values())
    if total_assigned < num_samples:
        samples_per_category['low'] += (num_samples - total_assigned)
    
    print(f"Generating {num_samples} synthetic execution plans...")
    print(f"Distribution: {samples_per_category}")
    
    plans = []
    plan_id = 1
    
    # Generate samples for each risk profile
    for risk_profile, count in samples_per_category.items():
        for _ in range(count):
            plan = generate_synthetic_plan(plan_id, risk_profile)
            plans.append(plan)
            plan_id += 1
    
    # Create DataFrame
    df = pd.DataFrame(plans)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df


def generate_edge_cases(num_samples=50):
    """
    Generate edge case execution plans for robustness testing
    
    Returns:
        DataFrame: Edge case execution plans
    """
    edge_cases = []
    
    for i in range(num_samples):
        # Vary edge conditions
        if i % 5 == 0:
            # Minimal execution
            plan = {
                'plan_id': f'edge_{i+1}',
                'num_steps': 1,
                'num_tools': 1,
                'tool_diversity': 1,
                'has_high_risk_tool': 0,
                'est_tokens': 500,
                'max_retries': 0,
                'sequential_tool_calls': 0,
                'plan_depth': 1,
                'time_limit_sec': 10,
                'failure_label': 0
            }
        elif i % 5 == 1:
            # Maximum complexity
            plan = {
                'plan_id': f'edge_{i+1}',
                'num_steps': 30,
                'num_tools': 15,
                'tool_diversity': 15,
                'has_high_risk_tool': 1,
                'est_tokens': 25000,
                'max_retries': 10,
                'sequential_tool_calls': 20,
                'plan_depth': 5,
                'time_limit_sec': 900,
                'failure_label': 2
            }
        elif i % 5 == 2:
            # High tokens, low steps (intensive operations)
            plan = {
                'plan_id': f'edge_{i+1}',
                'num_steps': random.randint(3, 6),
                'num_tools': random.randint(2, 4),
                'tool_diversity': random.randint(2, 4),
                'has_high_risk_tool': 1,
                'est_tokens': random.randint(12000, 18000),
                'max_retries': random.randint(1, 3),
                'sequential_tool_calls': random.randint(1, 3),
                'plan_depth': random.randint(1, 2),
                'time_limit_sec': random.randint(200, 400),
                'failure_label': 2
            }
        elif i % 5 == 3:
            # Many steps, low complexity (simple loops)
            plan = {
                'plan_id': f'edge_{i+1}',
                'num_steps': random.randint(15, 20),
                'num_tools': random.randint(2, 4),
                'tool_diversity': random.randint(2, 4),
                'has_high_risk_tool': 0,
                'est_tokens': random.randint(3000, 6000),
                'max_retries': random.randint(8, 12),
                'sequential_tool_calls': random.randint(10, 15),
                'plan_depth': random.randint(1, 2),
                'time_limit_sec': random.randint(150, 300),
                'failure_label': 2
            }
        else:
            # Borderline medium/high
            plan = {
                'plan_id': f'edge_{i+1}',
                'num_steps': random.randint(11, 13),
                'num_tools': random.randint(4, 6),
                'tool_diversity': random.randint(4, 6),
                'has_high_risk_tool': random.choice([0, 1]),
                'est_tokens': random.randint(8000, 10000),
                'max_retries': random.randint(3, 5),
                'sequential_tool_calls': random.randint(6, 9),
                'plan_depth': random.randint(2, 3),
                'time_limit_sec': random.randint(250, 350),
                'failure_label': random.choice([1, 2])
            }
        
        edge_cases.append(plan)
    
    return pd.DataFrame(edge_cases)


def save_synthetic_dataset(output_path, num_samples=1000, include_edge_cases=True):
    """
    Generate and save synthetic dataset
    
    Args:
        output_path: Path to save CSV
        num_samples: Number of regular samples
        include_edge_cases: Whether to include edge cases
    """
    # Generate main dataset
    df_main = generate_synthetic_dataset(num_samples)
    
    if include_edge_cases:
        # Generate edge cases
        df_edge = generate_edge_cases(50)
        # Combine
        df = pd.concat([df_main, df_edge], ignore_index=True)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    else:
        df = df_main
    
    # Reorder columns
    columns_order = [
        'plan_id',
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
    df = df[columns_order]
    
    # Save
    df.to_csv(output_path, index=False)
    
    print(f"\nGenerated {len(df)} synthetic execution plans")
    print(f"Saved to: {output_path}")
    
    # Print statistics
    print("\nRisk Label Distribution:")
    print(df['failure_label'].value_counts().sort_index())
    print("\nLabel Mapping:")
    print("  0 = LOW_RISK")
    print("  1 = MEDIUM_RISK")
    print("  2 = HIGH_RISK")
    
    print("\n" + "="*60)
    print("FEATURE SUMMARY STATISTICS")
    print("="*60)
    print(df.describe())
    
    return df


if __name__ == "__main__":
    output_csv = r"D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor\data\synthetic_plans.csv"
    df = save_synthetic_dataset(output_csv, num_samples=2000, include_edge_cases=True)
