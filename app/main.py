from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route 1 - Home page (serves HTML file now!)
@app.route("/")
def home():
    return render_template("index.html")   # ← renders your HTML page

# Route 2 - API response (used by the HTML page to hit)
@app.route("/api")
def api():
    return jsonify({
        "message": "Hello! My First Python App is Running!",
        "author": "Rishabh",
        "status": "running"
    })

# Route 3 - Health check
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })

# Route 4 - About
@app.route("/about")
def about():
    return jsonify({
        "app": "My First Python App",
        "built_with": "Flask",
        "purpose": "Learning Jenkins CI/CD"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)