"""
FastAPI service for Neural Execution Risk Predictor
Serves the trained model via REST API
"""
import os
import sys
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from tensorflow import keras

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import ExecutionPlanRequest, RiskPredictionResponse, HealthResponse

# Initialize FastAPI app
app = FastAPI(
    title="Neural Execution Risk Predictor API",
    description="Predicts runtime execution risk of autonomous agents before execution",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and scaler
model = None
scaler = None
feature_names = [
    'num_steps',
    'num_tools',
    'tool_diversity',
    'has_high_risk_tool',
    'est_tokens',
    'max_retries',
    'sequential_tool_calls',
    'plan_depth',
    'time_limit_sec'
]
risk_labels = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}


def load_model_and_scaler():
    """
    Load the trained model and scaler on startup
    """
    global model, scaler
    
    # Determine paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'model')
    
    model_path = os.path.join(model_dir, 'risk_model.h5')
    scaler_path = os.path.join(model_dir, 'scaler.joblib')
    
    try:
        # Load model
        print(f"Loading model from: {model_path}")
        model = keras.models.load_model(model_path)
        print("✓ Model loaded successfully")
        
        # Load scaler
        print(f"Loading scaler from: {scaler_path}")
        scaler = joblib.load(scaler_path)
        print("✓ Scaler loaded successfully")
        
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        raise


@app.on_event("startup")
async def startup_event():
    """
    Load model on API startup
    """
    print("="*60)
    print("Neural Execution Risk Predictor API - Starting Up")
    print("="*60)
    load_model_and_scaler()
    print("API ready to serve predictions!")
    print("="*60)


@app.get("/", response_model=dict)
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Neural Execution Risk Predictor API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict-risk (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        version="1.0.0"
    )


@app.post("/predict-risk", response_model=RiskPredictionResponse)
async def predict_risk(request: ExecutionPlanRequest):
    """
    Predict execution risk for an agent plan
    
    Args:
        request: ExecutionPlanRequest with plan features
        
    Returns:
        RiskPredictionResponse with risk level and confidence
    """
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    try:
        # Extract features in correct order
        features = np.array([[
            request.num_steps,
            request.num_tools,
            request.tool_diversity,
            int(request.has_high_risk_tool),  # Convert bool to int
            request.est_tokens,
            request.max_retries,
            request.sequential_tool_calls,
            request.plan_depth,
            request.time_limit_sec
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction_probs = model.predict(features_scaled, verbose=0)[0]
        predicted_class = int(np.argmax(prediction_probs))
        risk_score = float(prediction_probs[predicted_class])
        
        # Format response
        response = RiskPredictionResponse(
            risk_level=risk_labels[predicted_class],
            risk_score=risk_score,
            probabilities={
                "LOW": float(prediction_probs[0]),
                "MEDIUM": float(prediction_probs[1]),
                "HIGH": float(prediction_probs[2])
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/batch-predict", response_model=list[RiskPredictionResponse])
async def batch_predict(requests: list[ExecutionPlanRequest]):
    """
    Batch prediction for multiple execution plans
    
    Args:
        requests: List of ExecutionPlanRequest
        
    Returns:
        List of RiskPredictionResponse
    """
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )
    
    try:
        # Extract all features
        features_list = []
        for req in requests:
            features_list.append([
                req.num_steps,
                req.num_tools,
                req.tool_diversity,
                int(req.has_high_risk_tool),
                req.est_tokens,
                req.max_retries,
                req.sequential_tool_calls,
                req.plan_depth,
                req.time_limit_sec
            ])
        
        features = np.array(features_list)
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make predictions
        predictions_probs = model.predict(features_scaled, verbose=0)
        
        # Format responses
        responses = []
        for pred_probs in predictions_probs:
            predicted_class = int(np.argmax(pred_probs))
            risk_score = float(pred_probs[predicted_class])
            
            responses.append(RiskPredictionResponse(
                risk_level=risk_labels[predicted_class],
                risk_score=risk_score,
                probabilities={
                    "LOW": float(pred_probs[0]),
                    "MEDIUM": float(pred_probs[1]),
                    "HIGH": float(pred_probs[2])
                }
            ))
        
        return responses
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    print("Starting Neural Execution Risk Predictor API...")
    print("Access the API at: http://localhost:8000")
    print("Interactive docs at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
