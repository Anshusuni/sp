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

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["image_analysis"]
collection = db["images"]

# Load the trained model once
model = load_model("./b-h-1000.h5")

# Define the class labels your model was trained on
class_labels = ['Boron', 'healthy']

# Image preprocessing function
def preprocess_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((150, 150))  # Match training size
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize to [0, 1]
    return img_array

@app.route("/")
def home():
    return "Backend running"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        image_file = request.files['image']
        image_data = image_file.read()

        # Store image in MongoDB
        collection.insert_one({
            "filename": image_file.filename,
            "data": Binary(image_data)
        })

        processed = preprocess_image(image_data)
        prediction = model.predict(processed)

        predicted_index = np.argmax(prediction, axis=1)[0]
        predicted_class = class_labels[predicted_index]

        return jsonify({
            "filename": image_file.filename,
            "predicted_class": predicted_class,
            "raw_output": prediction.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
