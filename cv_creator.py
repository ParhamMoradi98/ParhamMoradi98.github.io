from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Sample CV chunks (replace with actual CV content)
cv_chunks = [
    "A strategic problem-solver who excels at translating mathematical concepts into practical solutions.",
    "Skilled Data Scientist with a strong background in ML, Optimization, Quantitative Analysis, and Mathematical Modeling.",
    "Master's Degree: Management and Data Sciences, University of Waterloo.",
    "Bachelor's Degree: B.Sc. in Computer Science & Electrical Engineering, Sharif University of Technology."
]

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert CV chunks to embeddings (vectors)
cv_embeddings = model.encode(cv_chunks)

# Convert the embeddings to numpy array and ensure the data type is float32 for Faiss
cv_embeddings = np.array(cv_embeddings).astype('float32')

# Initialize Faiss index (L2 distance metric)
embedding_dim = cv_embeddings.shape[1]  # 384 for 'all-MiniLM-L6-v2'
index = faiss.IndexFlatL2(embedding_dim)  # L2 distance is commonly used

# Add the embeddings to the Faiss index
index.add(cv_embeddings)

# Save the index to disk
faiss.write_index(index, 'cv_index.index')

print("Faiss index has been created and saved as 'cv_index.index'.")
