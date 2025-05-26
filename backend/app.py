from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import Binary
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["image_analysis"]
collection = db["images"]

# Load your model once
model = load_model("b-h-1000.h5")

# Dummy preprocessing — adjust based on your model’s input shape
def preprocess_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((150, 150))  # Example size, adjust as per your model
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize if your model expects it
    return img_array

@app.route("/")
def home():
    return "Backend running"

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image_file = request.files['image']
    image_data = image_file.read()

    # Store image in MongoDB
    collection.insert_one({
        "filename": image_file.filename,
        "data": Binary(image_data)
    })

    # Preprocess image
    processed = preprocess_image(image_data)

    # Predict using the model
    prediction = model.predict(processed)
    predicted_class = np.argmax(prediction, axis=1)[0]  # adjust depending on model

    # Dummy mapping — replace with your actual class labels
    labels = ['boron', 'healthy']
    result_label = labels[predicted_class] if predicted_class < len(labels) else str(predicted_class)

    return jsonify({
        "filename": image_file.filename,
        "predicted_class": result_label,
        "raw_output": prediction.tolist()
    })
