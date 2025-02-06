from flask import Flask, request, jsonify
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables (optional—remove if not needed)
load_dotenv()

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY is not set in environment variables.")

# ------------------------------------------------------------------------------
# 1) LOAD DATA & MODEL
# ------------------------------------------------------------------------------
# We assume 'cv_chunks.pkl' holds both text + embeddings to avoid recomputing them
with open("cv_chunks.pkl", "rb") as f:
    cv_data = pickle.load(f)

# Separate them into two arrays for convenient searching
cv_texts = [entry["text"] for entry in cv_data]
cv_embeddings = np.array([entry["embedding"] for entry in cv_data], dtype=np.float32)

# Use a smaller model than 'all-MiniLM-L6-v2' to reduce size
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

DEEPSEEK_CHAT_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

# ------------------------------------------------------------------------------
# 2) SEARCH FUNCTION (DOT-PRODUCT SIMILARITY)
# ------------------------------------------------------------------------------
def search_vector_db(query_embedding, top_k=3):
    """
    Simple vector search:
    - query_embedding: np.array of shape (768,) or similar
    - top_k: number of relevant chunks to fetch
    Returns:
       list of top_k CV chunk texts
    """
    # Convert to float32 if not already
    query_vec = query_embedding.astype(np.float32)
    
    # Dot product with all CV embeddings -> higher = more similar
    scores = np.dot(cv_embeddings, query_vec)  # shape: (num_chunks,)
    
    # Grab indices of the top_k scores
    top_indices = np.argsort(scores)[-top_k:][::-1]
    
    # Return the chunk texts that match best
    return [cv_texts[i] for i in top_indices]

# ------------------------------------------------------------------------------
# 3) FLASK ENDPOINT
# ------------------------------------------------------------------------------
@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "")
    
    # 3a) Embed the user's query
    question_embedding = model.encode([user_question])[0]
    
    # 3b) Find most relevant CV chunks
    relevant_chunks = search_vector_db(question_embedding, top_k=3)
    
    # 3c) Construct prompt and call DeepSeek
    prompt = f"Answer based on my CV: {relevant_chunks}\n\nQuestion: {user_question}"
    response = requests.post(
        DEEPSEEK_CHAT_ENDPOINT,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
        timeout=30
    )
    
    # 3d) Parse DeepSeek's response
    if response.status_code == 200:
        result_json = response.json()
        answer = result_json["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": "Failed to get a response from DeepSeek"}), 500

# ------------------------------------------------------------------------------
# 4) APP RUNNER
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000)
