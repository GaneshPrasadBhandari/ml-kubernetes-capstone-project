from flask import Flask, jsonify, send_from_directory

# Tell Flask where our static folder is
app = Flask(__name__, static_folder="static")


@app.route("/")
def home():
    return "<h1>Backend Flask App</h1><p>API is running!</p>"


@app.route("/api/hello")
def hello():
    """Simple JSON message for the assignment."""
    return jsonify({"message": "Hello from Flask backend via Kubernetes!"})


@app.route("/api/image")
def image():
    """
    Serve the image file through /api/image.
    This will return backend/static/myimage.jpg
    """
    filename = "myimage.jpg"
    return send_from_directory(app.static_folder, filename)


# Optional: also expose /static/<filename> in case you refer directly
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
