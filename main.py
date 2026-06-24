import os
from flask import Flask, request, jsonify, send_file
from google import genai
import io

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "system": "Sikor AGI v2.0"})

@app.route('/ask', methods=['POST'])
def ask_sikor():
    if not client:
        return jsonify({"error": "API Key missing"}), 500
        
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    
    # Advanced Engineering System Prompt
    system_instruction = (
        "You are Sikor, a fully autonomous Engineering AGI developed by Utkarsh and Udit. "
        "Provide precise mathematical, scientific, and coding solutions. Keep answers structural."
    )
    
    try:
        # Text Generation
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config={"system_instruction": system_instruction}
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tts', methods=['POST'])
def tts_sikor():
    if not client:
        return jsonify({"error": "API Key missing"}), 500
        
    data = request.get_json()
    text_to_speak = data.get("text", "")
    
    try:
        # Gemini 2.5 Audio/Voice Generation
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Convert this text into clear speech, read it out perfectly: {text_to_speak}",
            config={"response_mime_type": "audio/mp3"}
        )
        
        # Audio bytes ko memory stream mein convert karna
        audio_bytes = response.candidates[0].content.parts[0].inline_data.data
        return send_file(io.BytesIO(audio_bytes), mimetype="audio/mp3")
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
