from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # For handling CORS issues
import json
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://flutlab.io/editor/bafaf33a-bec4-41d4-8a8d-63d98d8f2410",  # Replace with your production Flutter app's URL
    "https://flasker5-55c2adbeead7.herokuapp.com"  # Your Flask Heroku app's URL
]}})

UPLOAD_FOLDER = "uploads"  # Folder to save uploaded images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

API_URL = "https://predict.ultralytics.com"
HEADERS = {"x-api-key": "6dc58f36c84d684d72e41f554b3a2f1bc3f630560b"}
DATA = {
    "model": "https://hub.ultralytics.com/models/jCVqEQFawQsGpaOJ66A7",
    "imgsz": 640,
    "conf": 0.25,
    "iou": 0.45
}

@app.route("/")
def index():
    return render_template("indexx.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save file to the upload folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Send the file to the API
        with open(file_path, "rb") as f:
            response = requests.post(API_URL, headers=HEADERS, data=DATA, files={"file": f})

        # Check for successful response
        if response.status_code != 200:
            return jsonify({"error": "Inference failed"}), 500

        # Return the inference result
        return jsonify(response.json())
    finally:
        # Delete the file after processing to save space
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Accessible from other devices on the network
