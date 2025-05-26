from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import Binary
import os
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image
import numpy as np
import io

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["image_analysis"]
collection = db["images"]

# Load model once
model = load_model("b-h-1000.h5")

# Define your two class names
class_labels = ['Boron', 'healthy']  # 🔁 Replace with your actual class names

def preprocess_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((150, 150))  # Match training size
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # normalize
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

    # Store image (optional)
    collection.insert_one({
        "filename": image_file.filename,
        "data": Binary(image_data)
    })

    # Predict
    processed = preprocess_image(image_data)
    prediction = model.predict(processed)

    # Binary classification
    predicted_index = np.argmax(prediction, axis=1)[0]
    predicted_class = class_labels[predicted_index]

    return jsonify({
        "filename": image_file.filename,
        "predicted_class": predicted_class,
        "raw_output": prediction.tolist()
    })
