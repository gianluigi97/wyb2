from flask import Flask, request, redirect, render_template, jsonify
import firebase_admin
from firebase_admin import auth, credentials

app = Flask(__name__)


cred = credentials.Certificate("whatdoyoubeer-firebase-adminsdk-fbsvc-f4984d6570.json") 
firebase_admin.initialize_app(cred)

@app.route('/')
def home():
    
    return render_template("index.html")

@app.route('/sessionLogin', methods=['POST'])
def session_login():
    data = request.get_json()
    id_token = data.get('idToken')

    try:
        # Verifica il token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        print(f"Utente autenticato: {uid}")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("Errore verifica token:", e)
        return jsonify({"error": "Invalid token"}), 401

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":

    app.run(debug=True)