from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<h1>Backend Flask App</h1><p>API is up and running!</p>"

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask backend!"})

if __name__ == "__main__":
    # Listen on all interfaces in the container
    app.run(host="0.0.0.0", port=5000)
