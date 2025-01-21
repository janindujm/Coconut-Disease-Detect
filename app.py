from flask import Flask, render_template, request, jsonify
import json
import requests
import os

app = Flask(__name__)
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
    return render_template("index.html")

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

    # Send the file to the API
    with open(file_path, "rb") as f:
        response = requests.post(API_URL, headers=HEADERS, data=DATA, files={"file": f})

    # Check for successful response
    if response.status_code != 200:
        return jsonify({"error": "Inference failed"}), 500

    # Delete the file after processing to save space
    os.remove(file_path)

    # Return the inference result
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
