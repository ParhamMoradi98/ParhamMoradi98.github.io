from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY is not set in environment variables.")

DEEPSEEK_CHAT_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

# Define your full CV as a constant string (or load from a file)
MY_FULL_CV = """
A strategic problem-solver who excels at translating mathematical concepts into practical solutions.
Skilled Data Scientist with a strong background in ML, Optimization, Quantitative Analysis, and Mathematical Modeling.
Master's Degree: Management and Data Sciences, University of Waterloo.
Bachelor's Degree: B.Sc. in Computer Science & Electrical Engineering, Sharif University of Technology.
"""

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "")
    
    # Create the prompt by including your full CV
    prompt = f"Imagine this is your CV:\n{MY_FULL_CV}\n\nAnswer the question:\n{user_question} Remember to answer with first person pronouns (I, me, my). not second person (you, your)."

    response = requests.post(
        DEEPSEEK_CHAT_ENDPOINT,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )

    if response.status_code == 200:
        result_json = response.json()
        answer = result_json["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": "Failed to get a response from DeepSeek"}), 500

if __name__ == "__main__":
    app.run(port=5000)
