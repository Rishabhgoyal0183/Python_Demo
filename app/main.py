from flask import Flask, jsonify

# Create the Flask application
app = Flask(__name__)

# Route 1 - Home page
@app.route("/")
def home():
    return jsonify({
        "message": "Hello! My First Python App is Running!",
        "author": "Rishabh",
        "status": "running"
    })

# Route 2 - Health check page
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })

# Route 3 - About page
@app.route("/about")
def about():
    return jsonify({
        "app": "My First Python App",
        "built_with": "Flask",
        "purpose": "Learning Jenkins CI/CD"
    })

# This runs the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)