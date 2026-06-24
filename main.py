import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Render ke environment variable se API key nikalna
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "active",
        "system": "Sikor",
        "developers": "Utkarsh & Udit",
        "date": "June 24, 2026"
    })

@app.route('/ask', methods=['POST'])
def ask_sikor():
    if not client:
        return jsonify({"error": "API Key missing on server"}), 500
        
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render automatic PORT assignment karta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
