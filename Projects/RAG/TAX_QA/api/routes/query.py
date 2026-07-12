"""
/query endpoint — routes user questions through the LangGraph orchestrator.
"""
from fastapi import APIRouter, HTTPException
from api.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main chat endpoint — processes questions through the full LangGraph pipeline:
    Intent Detection → Tax Engine → RAG Retrieval → Gemini → Answer
    """
    try:
        from recommendation_engine.graph import run_query

        result = run_query(
            user_query=request.question,
            mode=request.mode,
            tax_profile=request.tax_profile or {},
            form16_path=request.form16_path,
        )

        return QueryResponse(
            question=request.question,
            answer=result.get("final_answer", "") if isinstance(result, dict) else result.final_answer,
            citations=result.get("rag_context", {}).get("citations", "") if isinstance(result, dict) else (result.rag_context.citations if result.rag_context else ""),
            source_docs=result.get("rag_context", {}).get("source_docs", []) if isinstance(result, dict) else (result.rag_context.source_docs if result.rag_context else []),
            processing_steps=result.get("processing_steps", []) if isinstance(result, dict) else result.processing_steps,
            intent=result.get("intent", "tax_question") if isinstance(result, dict) else result.intent,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
