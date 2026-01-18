"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Literal


class ExecutionPlanRequest(BaseModel):
    """
    Request schema for execution plan risk prediction
    """
    num_steps: int = Field(..., ge=1, description="Number of execution steps")
    num_tools: int = Field(..., ge=1, description="Number of distinct tools used")
    tool_diversity: int = Field(..., ge=1, description="Diversity of tools")
    has_high_risk_tool: bool = Field(..., description="Flag for risky tools")
    est_tokens: int = Field(..., ge=0, description="Estimated token budget")
    max_retries: int = Field(..., ge=0, description="Maximum retry attempts")
    sequential_tool_calls: int = Field(..., ge=0, description="Consecutive repeated tool calls")
    plan_depth: int = Field(..., ge=1, le=5, description="Nesting depth (1-5)")
    time_limit_sec: int = Field(..., ge=0, description="Time limit in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "num_steps": 8,
                "num_tools": 3,
                "tool_diversity": 2,
                "has_high_risk_tool": True,
                "est_tokens": 7000,
                "max_retries": 2,
                "sequential_tool_calls": 4,
                "plan_depth": 2,
                "time_limit_sec": 120
            }
        }


class RiskPredictionResponse(BaseModel):
    """
    Response schema for risk prediction
    """
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = Field(..., description="Predicted risk level")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for prediction")
    probabilities: dict = Field(..., description="Probability distribution across all risk levels")
    
    class Config:
        json_schema_extra = {
            "example": {
                "risk_level": "HIGH",
                "risk_score": 0.82,
                "probabilities": {
                    "LOW": 0.05,
                    "MEDIUM": 0.13,
                    "HIGH": 0.82
                }
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response schema
    """
    status: str
    model_loaded: bool
    version: str
