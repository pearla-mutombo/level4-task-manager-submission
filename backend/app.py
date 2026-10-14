# Build this file together in Day 1.
# 1. Import Flask and jsonify.
# 2. Import CORS from flask_cors.
# 3. Create a Flask application named app.
# 4. Allow the supplied frontend origin for /api routes.
# 5. Define GET /api/health to return a JSON greeting.
# This starter intentionally cannot serve requests until those steps are complete.

# First we import Flask
from flask import Flask, jsonify

# Import new CORS library
from flask_cors import CORS

# Create a Flask application
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5173"}})

# Define endpoint name and below its functionality
@app.get("/api/health")
def health():
  return jsonify({"status": "ok", "message": "Hello from Flask"})

# Testing endpoint
@app.get("/api/me")
def me():
  return jsonify({"name": "Ulises", "favorite_color": "green"})
