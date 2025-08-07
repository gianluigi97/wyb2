from flask import Flask, request, redirect, render_template, jsonify, session, url_for
import firebase_admin
from firebase_admin import auth, credentials

app = Flask(__name__)


cred = credentials.Certificate("whatdoyoubeer-firebase-adminsdk-fbsvc-c9e162b42e.json") 
firebase_admin.initialize_app(cred)
app.secret_key = 'my-secret-key'

@app.route('/')
def home():
    if 'user' in session: 
        return redirect(url_for('dashboard'))

    return render_template("index.html")

@app.route('/sessionLogin', methods=['POST'])
def session_login():
    data = request.get_json()
    id_token = data.get('idToken')

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        session['user'] = uid
        print(f"Utente autenticato: {uid}")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("Errore verifica token:", e)
        return jsonify({"error": "Invalid token"}), 401

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():

    if 'user' not in session: 
        return redirect(url_for('home'))
    return render_template("dashboard.html")


if __name__ == "__main__":

    app.run(debug=True)
  