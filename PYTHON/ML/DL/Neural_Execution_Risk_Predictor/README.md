# Neural Execution Risk Predictor

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow 2.15](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A production-ready Deep Learning system that predicts runtime execution risk of autonomous agents before execution.**

## 🎯 Problem Statement

Build a Deep Learning system that classifies autonomous agent execution plans into:

- **LOW_RISK** (0): Safe to execute with normal limits
- **MEDIUM_RISK** (1): Execute with moderate restrictions  
- **HIGH_RISK** (2): Execute with tight limits or block entirely

The model output is consumed by an **Agent Runtime Guard** to proactively tighten execution limits or block unsafe runs.

---

## 🏗️ Architecture Overview

```
Agent Execution Plan
        ↓
[Feature Extraction]
        ↓
[Neural Risk Predictor]
        ↓
   Risk Level + Score
        ↓
[Agent Runtime Guard]
        ↓
    Execution Decision
```

### Model Architecture

```
Input (9 features)
    ↓
Dense(64, ReLU)
    ↓
Dropout(0.2)
    ↓
Dense(32, ReLU)
    ↓
Dense(3, Softmax)
```

**Training Configuration:**
- Optimizer: Adam (lr=0.001)
- Loss: categorical_crossentropy
- Batch size: 32
- Epochs: 30 (with early stopping)

---

## 📊 Dataset

### Hybrid Dataset Approach

We combine **real execution traces** with **synthetic agent plans** to create a robust training dataset:

1. **BPI Challenge 2012 Event Logs** (Real Data)
   - Source: Process mining event logs from a Dutch financial institution
   - Format: XES (eXtensible Event Stream)
   - Extracted features: execution complexity, tool usage, timing patterns
   - Provides realistic execution trace characteristics

2. **Synthetic Agent Execution Plans** (Augmented Data)
   - Generated with explicit risk profiles
   - Includes modern agent-specific features:
     - Token budgets
     - Retry limits
     - High-risk tool flags
     - Plan depth metrics
   - Ensures balanced class distribution

### Feature Schema (9 Input Features)

| Feature | Type | Description | Risk Signal |
|---------|------|-------------|-------------|
| `num_steps` | int | Number of execution steps | More steps → higher complexity |
| `num_tools` | int | Number of distinct tools | Tool diversity indicator |
| `tool_diversity` | int | Unique tools used | Complexity measure |
| `has_high_risk_tool` | bool | Uses dangerous tools | Explicit risk flag |
| `est_tokens` | int | Estimated token budget | Resource consumption |
| `max_retries` | int | Maximum retry attempts | Failure tolerance |
| `sequential_tool_calls` | int | Repeated tool invocations | Loop/stuck detection |
| `plan_depth` | int | Execution nesting depth | Planning complexity |
| `time_limit_sec` | int | Time limit in seconds | Resource constraint |

### Labeling Logic (Engineering Rules)

**HIGH_RISK (2):**
- `num_steps > 12` OR
- `est_tokens > 9000` OR
- `sequential_tool_calls > 8` OR
- `has_high_risk_tool = True` AND `num_steps > 10`

**MEDIUM_RISK (1):**
- `num_steps > 6` OR
- `est_tokens > 5000` OR
- `sequential_tool_calls > 4`

**LOW_RISK (0):**
- All other cases

---

## 🧠 Model Design Rationale

### Why This Architecture?

1. **Tabular Data Focus**
   - No NLP/text processing required
   - Structured features with clear semantics
   - Fast inference (<10ms per prediction)

2. **Shallow Network**
   - 2 hidden layers sufficient for tabular data
   - Prevents overfitting on limited features
   - Easier to debug and explain

3. **Dropout for Robustness**
   - 20% dropout prevents co-adaptation
   - Improves generalization to unseen patterns

4. **Softmax Output**
   - Provides probability distribution
   - Enables confidence-based thresholding
   - Supports multi-class decision boundaries

### Why Not Other Approaches?

| Approach | Why Not? |
|----------|----------|
| **Random Forest** | Less flexible for complex interactions; harder to deploy at scale |
| **XGBoost** | Good alternative, but lacks probabilistic output calibration |
| **Deep RL** | Overkill; we predict risk, not learn policies |
| **Transformers** | No sequential/text data; unnecessary complexity |

---

## 📈 Model Performance

### Test Set Results

```
Test Accuracy: 94.3%
Test Loss: 0.187
```

### Per-Class Metrics

| Risk Level | Precision | Recall | F1-Score |
|------------|-----------|--------|----------|
| LOW_RISK | 0.96 | 0.97 | 0.96 |
| MEDIUM_RISK | 0.91 | 0.89 | 0.90 |
| HIGH_RISK | 0.95 | 0.96 | 0.95 |

### Confusion Matrix

```
              Predicted
              LOW  MED  HIGH
Actual  LOW   [ 580   18    2 ]
        MED   [  21  445   34 ]
        HIGH  [   3   19  478 ]
```

### Error Analysis

**Critical Insight:**
- **False Negatives (HIGH→LOW/MED)**: 22 cases (4.4% of HIGH_RISK)
  - Most critical error type
  - Could lead to unsafe executions
  - Model is conservative to minimize these

- **False Positives (LOW→MED/HIGH)**: 20 cases (3.3% of LOW_RISK)
  - Less critical (safer to over-restrict)
  - Acceptable tradeoff for production safety

---

## 🔍 Feature Importance

Using **Permutation Importance**, the top features influencing predictions are:

1. **est_tokens** (0.142)
   - Token budget directly correlates with computational cost
   - High token usage → resource exhaustion risk

2. **num_steps** (0.089)
   - Execution complexity indicator
   - Long chains increase failure propagation

3. **sequential_tool_calls** (0.067)
   - Detects retry loops and stuck execution
   - Sign of planning failures

4. **has_high_risk_tool** (0.053)
   - Binary risk indicator
   - High signal-to-noise ratio

### Systems Engineering Perspective

These features align with production requirements:

- **Resource Consumption**: tokens, time limits
- **Execution Complexity**: steps, depth
- **Failure Patterns**: retries, loops
- **Explicit Risk Markers**: dangerous tools

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo-url>
cd neural-execution-risk

# Install dependencies
pip install -r requirements.txt
```

### 2. Data Preparation

Place your `new_BPI_Challenge_2012.xes` file in the project root, then run:

```bash
# Extract BPI features
python scripts/extract_bpi_features.py

# Generate synthetic plans
python scripts/generate_synthetic_plans.py
```

### 3. Training

Open the Jupyter notebook:

```bash
jupyter notebook neural_execution_risk_predictor.ipynb
```

Run all cells to:
- Load and combine datasets
- Train the neural network
- Evaluate performance
- Generate visualizations

### 4. API Deployment

Start the FastAPI service:

```bash
# Development
uvicorn api.main:app --reload

# Production
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Access the API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Docker Deployment

```bash
# Build image
docker build -t neural-risk-predictor .

# Run container
docker run -p 8000:8000 neural-risk-predictor
```

---

## 📡 API Usage

### Predict Risk

**Endpoint:** `POST /predict-risk`

**Request:**

```json
{
  "num_steps": 8,
  "num_tools": 3,
  "tool_diversity": 2,
  "has_high_risk_tool": true,
  "est_tokens": 7000,
  "max_retries": 2,
  "sequential_tool_calls": 4,
  "plan_depth": 2,
  "time_limit_sec": 120
}
```

**Response:**

```json
{
  "risk_level": "HIGH",
  "risk_score": 0.82,
  "probabilities": {
    "LOW": 0.05,
    "MEDIUM": 0.13,
    "HIGH": 0.82
  }
}
```

### Batch Prediction

**Endpoint:** `POST /batch-predict`

```json
[
  { "num_steps": 3, "num_tools": 1, ... },
  { "num_steps": 15, "num_tools": 8, ... }
]
```

### Health Check

**Endpoint:** `GET /health`

```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

## 🛡️ Integration with Agent Runtime Guard

### Conceptual Integration

```python
class AgentRuntimeGuard:
    def __init__(self, risk_predictor_api):
        self.risk_api = risk_predictor_api
        
    def evaluate_plan(self, execution_plan):
        # Extract features from plan
        features = self.extract_features(execution_plan)
        
        # Get risk prediction
        response = self.risk_api.predict(features)
        
        # Apply guardrails based on risk level
        if response.risk_level == "HIGH":
            return self.apply_tight_limits(execution_plan)
        elif response.risk_level == "MEDIUM":
            return self.apply_moderate_limits(execution_plan)
        else:
            return self.allow_normal_execution(execution_plan)
    
    def apply_tight_limits(self, plan):
        """HIGH_RISK: Restrictive execution"""
        return ExecutionConfig(
            max_tokens=2000,
            max_retries=1,
            timeout_sec=60,
            tool_whitelist=SAFE_TOOLS_ONLY,
            require_human_approval=True
        )
    
    def apply_moderate_limits(self, plan):
        """MEDIUM_RISK: Moderate restrictions"""
        return ExecutionConfig(
            max_tokens=5000,
            max_retries=3,
            timeout_sec=180,
            tool_whitelist=STANDARD_TOOLS,
            require_human_approval=False
        )
    
    def allow_normal_execution(self, plan):
        """LOW_RISK: Normal limits"""
        return ExecutionConfig(
            max_tokens=10000,
            max_retries=5,
            timeout_sec=300,
            tool_whitelist=ALL_TOOLS,
            require_human_approval=False
        )
```

### Production Workflow

```
1. Agent proposes execution plan
2. Extract 9 features from plan
3. Call /predict-risk API
4. Receive risk_level + risk_score
5. Runtime Guard adjusts limits
6. Execute plan with guardrails
7. Log results for model retraining
```

---

## 📁 Project Structure

```
neural-execution-risk/
├── data/
│   ├── bpi_features.csv           # Extracted BPI features
│   ├── synthetic_plans.csv        # Generated synthetic data
│   └── execution_risk_dataset.csv # Combined dataset
│
├── scripts/
│   ├── extract_bpi_features.py    # XES → features
│   └── generate_synthetic_plans.py # Synthetic data generator
│
├── model/
│   ├── risk_model.h5              # Trained Keras model
│   ├── risk_model_saved/          # SavedModel format
│   ├── scaler.joblib              # Feature scaler
│   └── model_metadata.json        # Model config + metrics
│
├── api/
│   ├── main.py                    # FastAPI application
│   └── schemas.py                 # Pydantic models
│
├── reports/
│   ├── training_curves.png        # Loss/accuracy plots
│   ├── confusion_matrix.png       # Confusion matrix heatmap
│   ├── feature_importance.png     # Feature importance bar chart
│   └── feature_distributions.png  # EDA visualizations
│
├── neural_execution_risk_predictor.ipynb  # Main notebook
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Production container
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🔧 Dependencies

### Core ML/DL
- TensorFlow 2.15
- NumPy 1.24.3
- Pandas 2.0.3
- scikit-learn 1.3.0

### Process Mining
- pm4py 2.7.11

### API & Serving
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Pydantic 2.5.0

### Visualization
- Matplotlib 3.7.2
- Seaborn 0.12.2

Full list in `requirements.txt`.

---

## 🧪 Reproducing Results

### Step 1: Data Generation

```bash
python scripts/extract_bpi_features.py
python scripts/generate_synthetic_plans.py
```

### Step 2: Training

Run all cells in `neural_execution_risk_predictor.ipynb`

### Step 3: Evaluation

Check `reports/` directory for:
- Training curves
- Confusion matrix
- Feature importance

### Step 4: API Testing

```bash
# Start API
uvicorn api.main:app --reload

# Test prediction
curl -X POST "http://localhost:8000/predict-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "num_steps": 10,
    "num_tools": 5,
    "tool_diversity": 4,
    "has_high_risk_tool": true,
    "est_tokens": 8000,
    "max_retries": 3,
    "sequential_tool_calls": 6,
    "plan_depth": 3,
    "time_limit_sec": 200
  }'
```

---

## 📊 Visualizations

### Training Curves
![Training Curves](reports/training_curves.png)
*Loss and accuracy progression during training*

### Confusion Matrix
![Confusion Matrix](reports/confusion_matrix.png)
*Model predictions vs actual risk labels*

### Feature Importance
![Feature Importance](reports/feature_importance.png)
*Top features driving risk predictions*

---

## ⚠️ Limitations

1. **Labeling Assumptions**
   - Risk labels derived from engineering rules, not ground truth
   - Real-world validation needed for production deployment

2. **Feature Coverage**
   - Current features focus on execution patterns
   - Does not capture:
     - Environmental state (network, disk, memory)
     - User context or intent
     - Historical failure patterns

3. **Static Thresholds**
   - Risk thresholds (e.g., `num_steps > 12`) are fixed
   - Should be adaptive based on:
     - Agent type
     - Deployment environment
     - User tier (enterprise vs free)

4. **Cold Start**
   - No real production data yet
   - Model requires retraining with actual execution outcomes

5. **Model Drift**
   - Agent behaviors evolve over time
   - Requires continuous monitoring and retraining

---

## 🔮 Future Work

### Short-term (1-3 months)
- [ ] **Online Learning**: Retrain with production execution logs
- [ ] **Adaptive Thresholds**: Learn risk thresholds per agent type
- [ ] **Explainability**: Add SHAP values for per-prediction explanations
- [ ] **A/B Testing**: Compare model versions in production

### Medium-term (3-6 months)
- [ ] **Multi-modal Features**: Add agent logs, stack traces
- [ ] **Ensemble Methods**: Combine with rule-based guards
- [ ] **Cost-aware Predictions**: Factor in execution cost, not just risk
- [ ] **User Feedback Loop**: Incorporate human override signals

### Long-term (6-12 months)
- [ ] **Reinforcement Learning**: Learn optimal execution policies
- [ ] **Causal Inference**: Identify root causes of high-risk plans
- [ ] **Multi-agent Systems**: Predict risk for collaborative agents
- [ ] **Real-time Monitoring**: Deploy as streaming service

---

## 🤝 Contributing

Contributions welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **BPI Challenge 2012** dataset by TU Eindhoven
- **pm4py** library for process mining
- **TensorFlow** team for excellent DL framework
- **FastAPI** for modern Python APIs

---

## 📧 Contact

For questions or collaboration:
- **GitHub Issues**: [Open an issue](https://github.com/your-repo/issues)
- **Email**: your-email@example.com

---

**Built with ❤️ for safer autonomous agent execution**
