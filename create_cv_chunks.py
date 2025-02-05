import pickle

# Sample CV chunks (you can replace this with actual content from your CV)
cv_chunks = [
    "A strategic problem-solver who excels at translating mathematical concepts into practical solutions.",
    "Skilled Data Scientist with a strong background in ML, Optimization, Quantitative Analysis, and Mathematical Modeling.",
    "Master's Degree: Management and Data Sciences, University of Waterloo.",
    "Bachelor's Degree: B.Sc. in Computer Science & Electrical Engineering, Sharif University of Technology."
]

# Save the CV chunks to a pickle file
with open('cv_chunks.pkl', 'wb') as f:
    pickle.dump(cv_chunks, f)

print("cv_chunks.pkl file has been created successfully!")
