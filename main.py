from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
        
    response = client.responses.create(
        model="gpt-5.4",
        input=[
                {"role": "system", "content": "Act like a helpful personal assistant"},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_output_tokens=512
    )
        
    answer = response.output_text.strip()
    return jsonify({"response": answer}), 200

@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email")
    prompt = f"summarize the following email in 2-3 sentences: {email_text}"
        
    response = client.responses.create(
        model="gpt-5.4",
        input=[
                {"role": "system", "content": "Act like an expert email assistant"},                
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_output_tokens=512
    )
        
    summary = response.output_text.strip()
    return jsonify({"response": summary}), 200

if __name__ == "__main__":
    app.run(debug=True)

