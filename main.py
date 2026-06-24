import os
from flask import Flask, request, jsonify

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    from google import genai
    client = genai.Client(api_key=api_key)
else:
    client = None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "system": "Sikor AGI v2.0"})

@app.route('/ask', methods=['POST'])
def ask_sikor():
    if not client:
        return jsonify({"error": "API Key missing"}), 500
        
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    
    system_instruction = (
        "You are Sikor, a fully autonomous Engineering AGI developed by Utkarsh and Udit. "
        "Provide precise mathematical, scientific, and coding solutions."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config={"system_instruction": system_instruction}
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
