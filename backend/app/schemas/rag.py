from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class RAGSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    category: Optional[str] = None

class RAGSearchResult(BaseModel):
    text: str
    source: str
    category: str
    score: float
    metadata: Optional[Dict[str, Any]] = None

class RAGSearchResponse(BaseModel):
    query: str
    results: List[RAGSearchResult]
    total_found: int
