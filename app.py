from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import re

app = Flask(__name__)
CORS(app)

# API Key Konfiguration
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.get_json()
        user_text = data.get("text")
        
        if not user_text:
            return jsonify({"kcal": 0, "note": "Kein Text empfangen"}), 400

        prompt = f"Wie viele Kalorien hat: '{user_text}'? Gib NUR die Zahl zurück. Falls unbekannt, gib 0."
        
        response = model.generate_content(prompt)
        
        # Extrahiere alle Zahlen aus der Antwort der KI
        nums = re.findall(r'\d+', response.text)
        kcal = int(nums[0]) if nums else 0
        
        return jsonify({"kcal": kcal})

    except Exception as e:
        # Dies schreibt den genauen Fehler in die Render-Logs
        print(f"FEHLER: {str(e)}")
        return jsonify({"error": "KI-Fehler", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
