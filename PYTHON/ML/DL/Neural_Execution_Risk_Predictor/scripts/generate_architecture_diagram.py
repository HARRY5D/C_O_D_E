"""
System Architecture Diagram Generator
Creates a visual representation of the Neural Execution Risk Predictor system
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os


def create_architecture_diagram():
    """Create system architecture diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(5, 11.5, 'Neural Execution Risk Predictor - System Architecture',
            ha='center', va='top', fontsize=16, fontweight='bold')
    
    # Colors
    color_data = '#E3F2FD'
    color_model = '#FFF3E0'
    color_api = '#E8F5E9'
    color_runtime = '#FCE4EC'
    
    # 1. Data Layer
    ax.add_patch(FancyBboxPatch((0.5, 9), 4, 1.5, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='#1976D2', facecolor=color_data, linewidth=2))
    ax.text(2.5, 10.2, 'Data Sources', ha='center', fontweight='bold', fontsize=11)
    ax.text(2.5, 9.7, 'BPI Challenge 2012 (XES)', ha='center', fontsize=9)
    ax.text(2.5, 9.4, 'Synthetic Execution Plans', ha='center', fontsize=9)
    
    # 2. Feature Engineering
    ax.add_patch(FancyBboxPatch((5.5, 9), 4, 1.5,
                                boxstyle="round,pad=0.1",
                                edgecolor='#1976D2', facecolor=color_data, linewidth=2))
    ax.text(7.5, 10.2, 'Feature Extraction', ha='center', fontweight='bold', fontsize=11)
    ax.text(7.5, 9.7, '9 Structured Features', ha='center', fontsize=9)
    ax.text(7.5, 9.4, 'StandardScaler Normalization', ha='center', fontsize=9)
    
    # Arrow: Data → Features
    arrow1 = FancyArrowPatch((4.5, 9.75), (5.5, 9.75),
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#1976D2')
    ax.add_patch(arrow1)
    
    # 3. Neural Network Model
    ax.add_patch(FancyBboxPatch((2, 6.5), 6, 2,
                                boxstyle="round,pad=0.1",
                                edgecolor='#F57C00', facecolor=color_model, linewidth=2))
    ax.text(5, 8.2, 'Deep Neural Network', ha='center', fontweight='bold', fontsize=12)
    ax.text(5, 7.8, 'Input (9) → Dense(64) → Dropout(0.2) → Dense(32) → Softmax(3)',
            ha='center', fontsize=9, family='monospace')
    ax.text(5, 7.4, 'Output: [LOW_RISK, MEDIUM_RISK, HIGH_RISK]',
            ha='center', fontsize=9)
    ax.text(5, 7.0, 'Training: Adam, categorical_crossentropy, early stopping',
            ha='center', fontsize=8, style='italic')
    
    # Arrow: Features → Model
    arrow2 = FancyArrowPatch((5, 9), (5, 8.5),
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#F57C00')
    ax.add_patch(arrow2)
    
    # 4. Model Artifacts
    ax.add_patch(FancyBboxPatch((0.5, 4.8), 3.5, 1.2,
                                boxstyle="round,pad=0.05",
                                edgecolor='#F57C00', facecolor=color_model, linewidth=1.5))
    ax.text(2.25, 5.7, 'Saved Artifacts', ha='center', fontweight='bold', fontsize=10)
    ax.text(2.25, 5.35, 'risk_model.h5', ha='center', fontsize=8, family='monospace')
    ax.text(2.25, 5.05, 'scaler.joblib', ha='center', fontsize=8, family='monospace')
    
    # 5. FastAPI Service
    ax.add_patch(FancyBboxPatch((5.5, 4.5), 4, 1.8,
                                boxstyle="round,pad=0.1",
                                edgecolor='#388E3C', facecolor=color_api, linewidth=2))
    ax.text(7.5, 6.1, 'FastAPI Service', ha='center', fontweight='bold', fontsize=11)
    ax.text(7.5, 5.7, 'POST /predict-risk', ha='center', fontsize=9, family='monospace')
    ax.text(7.5, 5.4, 'POST /batch-predict', ha='center', fontsize=9, family='monospace')
    ax.text(7.5, 5.1, 'GET /health', ha='center', fontsize=9, family='monospace')
    ax.text(7.5, 4.8, 'Docker Container Ready', ha='center', fontsize=8, style='italic')
    
    # Arrow: Model → API
    arrow3 = FancyArrowPatch((5, 6.5), (6.5, 6.3),
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#388E3C')
    ax.add_patch(arrow3)
    
    # 6. Agent Runtime Guard
    ax.add_patch(FancyBboxPatch((2, 2.5), 6, 1.8,
                                boxstyle="round,pad=0.1",
                                edgecolor='#C2185B', facecolor=color_runtime, linewidth=2))
    ax.text(5, 4.1, 'Agent Runtime Guard', ha='center', fontweight='bold', fontsize=12)
    ax.text(5, 3.7, 'Risk Assessment → Execution Policy', ha='center', fontsize=9)
    ax.text(5, 3.3, 'HIGH: Tight Limits | MEDIUM: Moderate | LOW: Normal',
            ha='center', fontsize=8)
    ax.text(5, 2.9, 'Proactive Safety Enforcement', ha='center', fontsize=8, style='italic')
    
    # Arrow: API → Runtime Guard
    arrow4 = FancyArrowPatch((7.5, 4.5), (5, 4.3),
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#C2185B')
    ax.add_patch(arrow4)
    
    # 7. Agent Execution
    ax.add_patch(FancyBboxPatch((2, 0.5), 6, 1.5,
                                boxstyle="round,pad=0.1",
                                edgecolor='#424242', facecolor='#EEEEEE', linewidth=2))
    ax.text(5, 1.8, 'Safe Agent Execution', ha='center', fontweight='bold', fontsize=11)
    ax.text(5, 1.4, 'With Applied Guardrails & Limits', ha='center', fontsize=9)
    ax.text(5, 1.0, '✓ Token Budget | ✓ Retry Limits | ✓ Time Constraints',
            ha='center', fontsize=8)
    ax.text(5, 0.7, '✓ Tool Whitelisting | ✓ Human Approval (if HIGH)',
            ha='center', fontsize=8)
    
    # Arrow: Runtime Guard → Execution
    arrow5 = FancyArrowPatch((5, 2.5), (5, 2.0),
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#424242')
    ax.add_patch(arrow5)
    
    # Side annotations
    ax.text(0.2, 9.75, '1', fontsize=14, fontweight='bold', color='#1976D2')
    ax.text(0.2, 7.5, '2', fontsize=14, fontweight='bold', color='#F57C00')
    ax.text(0.2, 5.5, '3', fontsize=14, fontweight='bold', color='#388E3C')
    ax.text(0.2, 3.5, '4', fontsize=14, fontweight='bold', color='#C2185B')
    ax.text(0.2, 1.5, '5', fontsize=14, fontweight='bold', color='#424242')
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=color_data, edgecolor='#1976D2', label='Data Pipeline'),
        mpatches.Patch(facecolor=color_model, edgecolor='#F57C00', label='ML Model'),
        mpatches.Patch(facecolor=color_api, edgecolor='#388E3C', label='API Layer'),
        mpatches.Patch(facecolor=color_runtime, edgecolor='#C2185B', label='Runtime Guard'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Create diagram
    fig = create_architecture_diagram()
    
    # Save
    output_path = os.path.join(
        r"D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor",
        "reports",
        "system_architecture.png"
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    print(f"✓ System architecture diagram saved to: {output_path}")
    plt.show()
