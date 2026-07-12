"""
FinAssist AI — FastAPI Application Entry Point
LangSmith tracing is automatically enabled via environment variables.
"""
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.langsmith_config import configure_langsmith
from api.routes import health, query, tax, form16


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup tasks — configure LangSmith before accepting requests."""
    configure_langsmith()
    print("✅ LangSmith tracing configured")
    print("✅ FinAssist AI API starting up...")
    yield
    print("👋 FinAssist AI API shutting down")


app = FastAPI(
    title="FinAssist AI",
    description="Intelligent Indian Tax Planning Assistant — FY 2025-26",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(query.router, tags=["RAG Query"])
app.include_router(tax.router, tags=["Tax Engine"])
app.include_router(form16.router, tags=["Form 16"])


@app.get("/")
async def root():
    return {
        "message": "FinAssist AI — Indian Tax Planning Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    from config.settings import settings

    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
