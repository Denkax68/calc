from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app) # Erlaubt Anfragen von deinem Handy

# Den API Key ziehen wir aus den Umgebungsvariablen (sicherer!)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    user_text = data.get("text")
    
    prompt = f"Du bist ein Ernährungsberater. Der Nutzer sagt: '{user_text}'. " \
             f"Gib NUR die geschätzte Kalorienanzahl als Zahl zurück. " \
             f"Falls es mehrere Dinge sind, addiere sie. Wenn du es nicht weißt, gib '0' zurück."
    
    try:
        response = model.generate_content(prompt)
        # Wir filtern nur die Zahlen aus der Antwort
        kcal = "".join(filter(str.isdigit, response.text))
        return jsonify({"kcal": int(kcal) if kcal else 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
