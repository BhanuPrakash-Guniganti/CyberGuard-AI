from fastapi import APIRouter
from typing import List
from backend.app.schemas.rag import RAGSearchRequest, RAGSearchResponse, RAGSearchResult
from backend.app.rag.retriever import rag_retriever

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Base"])

@router.post("/search", response_model=RAGSearchResponse)
async def search_knowledge_base(req: RAGSearchRequest):
    results_raw = rag_retriever.search(query=req.query, top_k=req.top_k)
    
    results = [
        RAGSearchResult(
            text=r["text"],
            source=r["source"],
            category=r["category"],
            score=r["score"],
            metadata={"chunk_id": r.get("chunk_id")}
        )
        for r in results_raw
    ]

    return RAGSearchResponse(
        query=req.query,
        results=results,
        total_found=len(results)
    )
