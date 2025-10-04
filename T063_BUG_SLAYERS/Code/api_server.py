
# api_server.py
import os, json, time
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import faiss, numpy as np
from sentence_transformers import SentenceTransformer
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# load index and passages
index = faiss.read_index("faiss.index")
with open("passages.json","r",encoding="utf8") as f:
    passages = json.load(f)

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(question, k=4):
    q_emb = embedder.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, k)
    results = []
    for idx in I[0]:
        if idx < len(passages):
            results.append(passages[idx])
    return results

def make_prompt(question, retrieved):
    context = "\n\n---\n".join([f"Title: {r['title']}\nText: {r['text']}" for r in retrieved])
    prompt = f"""You are an assistant for the Student Portal. Use ONLY the information in the context to answer the question. If the answer is not contained, say you don't know and suggest where to check.

Context:
{context}

Question: {question}

Answer concisely, step-by-step if needed. Also include a 'sources' list referencing titles from the context.
"""
    return prompt

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    q = data.get("question","").strip()
    if not q:
        return jsonify({"error":"no question"}), 400

    retrieved = retrieve(q, k=4)
    prompt = make_prompt(q, retrieved)

    # call OpenAI completion (choose model you have access to)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini", # replace with available model
        messages=[{"role":"user","content":prompt}],
        max_tokens=400,
        temperature=0.1
    )
    answer = resp["choices"][0]["message"]["content"].strip()

    return jsonify({
        "question": q,
        "answer": answer,
        "retrieved": retrieved
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)
