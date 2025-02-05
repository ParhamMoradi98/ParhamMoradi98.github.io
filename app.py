from flask import Flask, request, jsonify
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for the entire Flask app
CORS(app)
# Load your Faiss index and CV chunks
index = faiss.read_index('cv_index.index')
with open('cv_chunks.pkl', 'rb') as f:
    cv_chunks = pickle.load(f)

# Initialize the Sentence Transformer model for embedding queries
model = SentenceTransformer('all-MiniLM-L6-v2')

DEEPSEEK_API_KEY = "sk-749fbf313e854f2a92d5397d334c3b14"
DEEPSEEK_CHAT_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

def search_vector_db(query_embedding, top_k=3):
    """
    Searches the vector database (Faiss index) for the most relevant CV chunks 
    based on the user's query embedding.

    Args:
        query_embedding (list or np.ndarray): The query embedding (user's question)
        top_k (int): The number of top results to return

    Returns:
        list: The most relevant CV chunks
    """
    # Ensure the query embedding is a numpy array and of type float32 for Faiss
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)

    # Perform the similarity search in the Faiss index
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve the most relevant CV chunks using the indices
    relevant_chunks = [cv_chunks[i] for i in indices[0]]
    
    return relevant_chunks

def get_deepseek_embedding(text):
    # Call DeepSeek's embedding API here to get the embedding for the user's query
    pass

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json['question']
    
    # Step 1: Retrieve relevant CV chunks
    question_embedding = model.encode([user_question])[0]
    cv_chunks = search_vector_db(question_embedding, top_k=3)
    
    # Step 2: Generate answer using DeepSeek
    prompt = f"Answer based on my CV: {cv_chunks}\n\nQuestion: {user_question}"
    response = requests.post(
        DEEPSEEK_CHAT_ENDPOINT,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    )
    answer = response.json()['choices'][0]['message']['content']
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(port=5000)
