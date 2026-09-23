import os
import joblib
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.metrics.pairwise import cosine_similarity

INDEX_DIR = os.path.join(os.path.dirname(__file__), "index_store")

class RAGRetriever:
    def __init__(self):
        self.vectorizer = None
        self.embeddings = None
        self.chunks = None
        self.is_loaded = False
        self._load_index()

    def _load_index(self):
        try:
            vec_path = os.path.join(INDEX_DIR, "vectorizer.joblib")
            emb_path = os.path.join(INDEX_DIR, "embeddings.joblib")
            chk_path = os.path.join(INDEX_DIR, "chunks.joblib")
            
            if os.path.exists(vec_path) and os.path.exists(emb_path) and os.path.exists(chk_path):
                self.vectorizer = joblib.load(vec_path)
                self.embeddings = joblib.load(emb_path)
                self.chunks = joblib.load(chk_path)
                self.is_loaded = True
            else:
                self.is_loaded = False
        except Exception as e:
            print(f"[-] Error loading RAG index: {e}")
            self.is_loaded = False

    def search(self, query: str, top_k: int = 5, min_score: float = 0.05) -> List[Dict[str, Any]]:
        if not self.is_loaded:
            self._load_index()

        if not self.is_loaded or not self.chunks:
            return []

        # Vectorize query
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.embeddings)[0]

        # Top indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= min_score:
                chunk = self.chunks[idx]
                results.append({
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "category": chunk["category"],
                    "score": round(score, 4),
                    "chunk_id": chunk.get("chunk_id")
                })
        return results

rag_retriever = RAGRetriever()
