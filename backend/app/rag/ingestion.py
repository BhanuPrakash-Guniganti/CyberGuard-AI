import os
import glob
import re
import joblib
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge_base")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "index_store")

def extract_chunks_from_markdown(file_path: str, chunk_size: int = 400) -> List[Dict[str, Any]]:
    chunks = []
    file_name = os.path.basename(file_path)
    category = file_name.replace(".md", "").replace("_", " ").title()
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on markdown headers or double newlines
    sections = re.split(r'\n(?=#{1,3}\s)', content)
    for sec_idx, section in enumerate(sections):
        cleaned = section.strip()
        if not cleaned:
            continue
        
        # Sub-chunk if section is too long
        words = cleaned.split()
        if len(words) > 120:
            for i in range(0, len(words), 80):
                sub_chunk = " ".join(words[i:i+100])
                chunks.append({
                    "chunk_id": f"{file_name}_sec{sec_idx}_{i}",
                    "text": sub_chunk,
                    "source": file_name,
                    "category": category
                })
        else:
            chunks.append({
                "chunk_id": f"{file_name}_sec{sec_idx}",
                "text": cleaned,
                "source": file_name,
                "category": category
            })

    return chunks

def build_and_save_index():
    print("[*] Ingesting documents from knowledge_base/ ...")
    md_files = glob.glob(os.path.join(KB_DIR, "*.md"))
    if not md_files:
        print(f"[-] No markdown files found in {KB_DIR}")
        return

    all_chunks = []
    for fpath in md_files:
        chunks = extract_chunks_from_markdown(fpath)
        all_chunks.extend(chunks)
        print(f" [+] Ingested {len(chunks)} chunks from {os.path.basename(fpath)}")

    texts = [c["text"] for c in all_chunks]
    
    # Use high-dimensional TF-IDF vector space with sublinear term frequency
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        stop_words="english",
        sublinear_tf=True,
        min_df=1
    )
    embeddings = vectorizer.fit_transform(texts)

    os.makedirs(INDEX_DIR, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(INDEX_DIR, "vectorizer.joblib"))
    joblib.dump(embeddings, os.path.join(INDEX_DIR, "embeddings.joblib"))
    joblib.dump(all_chunks, os.path.join(INDEX_DIR, "chunks.joblib"))
    
    print(f"[+] Successfully built RAG index with {len(all_chunks)} chunks in {INDEX_DIR}")

if __name__ == "__main__":
    build_and_save_index()
