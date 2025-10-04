# ingest_and_build_faiss.py
import os, json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL_NAME)

# --- load source documents: assume a JSONL file with {"id","title","content"}
with open("docs.jsonl","r",encoding="utf8") as f:
    docs = [json.loads(line) for line in f]

# chunking: simple split by sentences/paragraphs
passages = []
for d in docs:
    content = d["content"].strip()
    # naive split by sentences/paragraphs
    chunks = [p.strip() for p in content.split("\n") if p.strip()]
    if not chunks:
        chunks = [content]
    for i, chunk in enumerate(chunks):
        passages.append({
            "doc_id": d["id"],
            "title": d.get("title",""),
            "text": chunk
        })

texts = [p["text"] for p in passages]
embs = embedder.encode(texts, convert_to_numpy=True, show_progress_bar=True)

# build faiss index
dim = embs.shape[1]
index = faiss.IndexFlatIP(dim)          # cosine works if vectors normalized
faiss.normalize_L2(embs)
index.add(embs)
faiss.write_index(index, "faiss.index")

# save passages metadata
with open("passages.json","w",encoding="utf8") as f:
    json.dump(passages, f, ensure_ascii=False, indent=2)
print("Built faiss.index and passages.json")
