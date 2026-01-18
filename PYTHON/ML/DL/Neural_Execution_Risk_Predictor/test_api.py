"""
Simple API client example for testing the Neural Execution Risk Predictor
"""
import requests
import json


def test_predict_risk():
    """Test the /predict-risk endpoint"""
    url = "http://localhost:8000/predict-risk"
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Safe Execution",
            "data": {
                "num_steps": 3,
                "num_tools": 2,
                "tool_diversity": 2,
                "has_high_risk_tool": False,
                "est_tokens": 1500,
                "max_retries": 1,
                "sequential_tool_calls": 0,
                "plan_depth": 1,
                "time_limit_sec": 60
            }
        },
        {
            "name": "Moderate Complexity",
            "data": {
                "num_steps": 8,
                "num_tools": 4,
                "tool_diversity": 4,
                "has_high_risk_tool": True,
                "est_tokens": 6000,
                "max_retries": 3,
                "sequential_tool_calls": 2,
                "plan_depth": 2,
                "time_limit_sec": 180
            }
        },
        {
            "name": "High-Risk Execution",
            "data": {
                "num_steps": 18,
                "num_tools": 8,
                "tool_diversity": 7,
                "has_high_risk_tool": True,
                "est_tokens": 15000,
                "max_retries": 6,
                "sequential_tool_calls": 12,
                "plan_depth": 4,
                "time_limit_sec": 500
            }
        }
    ]
    
    print("="*60)
    print("Testing Neural Execution Risk Predictor API")
    print("="*60)
    
    for test in test_cases:
        print(f"\nTest Case: {test['name']}")
        print(f"Input: {json.dumps(test['data'], indent=2)}")
        
        try:
            response = requests.post(url, json=test['data'])
            response.raise_for_status()
            
            result = response.json()
            print(f"\n✓ Prediction: {result['risk_level']}")
            print(f"  Confidence: {result['risk_score']:.2%}")
            print(f"  Probabilities:")
            print(f"    LOW:    {result['probabilities']['LOW']:.3f}")
            print(f"    MEDIUM: {result['probabilities']['MEDIUM']:.3f}")
            print(f"    HIGH:   {result['probabilities']['HIGH']:.3f}")
            
        except requests.exceptions.RequestException as e:
            print(f"\n✗ Error: {e}")
        
        print("-" * 60)


def test_health_check():
    """Test the /health endpoint"""
    url = "http://localhost:8000/health"
    
    print("\nTesting Health Check Endpoint...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        print(f"✓ Status: {result['status']}")
        print(f"  Model Loaded: {result['model_loaded']}")
        print(f"  Version: {result['version']}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")


def test_batch_predict():
    """Test the /batch-predict endpoint"""
    url = "http://localhost:8000/batch-predict"
    
    batch_data = [
        {
            "num_steps": 5,
            "num_tools": 2,
            "tool_diversity": 2,
            "has_high_risk_tool": False,
            "est_tokens": 2000,
            "max_retries": 1,
            "sequential_tool_calls": 1,
            "plan_depth": 1,
            "time_limit_sec": 90
        },
        {
            "num_steps": 12,
            "num_tools": 6,
            "tool_diversity": 5,
            "has_high_risk_tool": True,
            "est_tokens": 8000,
            "max_retries": 4,
            "sequential_tool_calls": 7,
            "plan_depth": 3,
            "time_limit_sec": 250
        }
    ]
    
    print("\n" + "="*60)
    print("Testing Batch Prediction Endpoint")
    print("="*60)
    print(f"\nSending {len(batch_data)} requests...")
    
    try:
        response = requests.post(url, json=batch_data)
        response.raise_for_status()
        
        results = response.json()
        
        for i, result in enumerate(results, 1):
            print(f"\nPrediction {i}:")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Confidence: {result['risk_score']:.2%}")
        
        print("\n✓ Batch prediction successful!")
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Neural Execution Risk Predictor - API Client Test")
    print("="*60)
    print("\nMake sure the API is running at http://localhost:8000")
    print("Start it with: uvicorn api.main:app --reload")
    print()
    
    input("Press Enter to start tests...")
    
    # Run tests
    test_health_check()
    test_predict_risk()
    test_batch_predict()
    
    print("\n" + "="*60)
    print("All tests complete!")
    print("="*60)
