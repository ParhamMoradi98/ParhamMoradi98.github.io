import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------------------------
# 1) SAMPLE CV CHUNKS (Replace with actual CV content)
# ------------------------------------------------------------------------------
cv_texts = [
    "A strategic problem-solver who excels at translating mathematical concepts into practical solutions.",
    "Skilled Data Scientist with a strong background in ML, Optimization, Quantitative Analysis, and Mathematical Modeling.",
    "Master's Degree: Management and Data Sciences, University of Waterloo.",
    "Bachelor's Degree: B.Sc. in Computer Science & Electrical Engineering, Sharif University of Technology."
]

# ------------------------------------------------------------------------------
# 2) CREATE EMBEDDINGS
#    (Use a smaller Sentence Transformer model to reduce size if needed)
# ------------------------------------------------------------------------------
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")
cv_embeddings = model.encode(cv_texts)             # shape: (num_chunks, embedding_dim)
cv_embeddings = np.array(cv_embeddings).astype(np.float32)

# ------------------------------------------------------------------------------
# 3) COMBINE TEXT + EMBEDDINGS INTO A SINGLE LIST OF DICTIONARIES
# ------------------------------------------------------------------------------
cv_data = []
for text, emb in zip(cv_texts, cv_embeddings):
    # Convert numpy array -> list of floats for serialization
    cv_data.append({
        "text": text,
        "embedding": emb.tolist()
    })

# ------------------------------------------------------------------------------
# 4) SAVE AS PICKLE
# ------------------------------------------------------------------------------
with open("cv_chunks.pkl", "wb") as f:
    pickle.dump(cv_data, f)

print("cv_chunks.pkl has been created successfully!")
