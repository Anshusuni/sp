from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import Binary
import os
from dotenv import load_dotenv
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image
import numpy as np
import io

import cv2

# Read and display the background image
img = cv2.imread('background.jpg')
cv2.imshow("Background Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()



# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["image_analysis"]
collection = db["images"]

# Class labels
class_labels = ['Boron', 'healthy']

# Preprocessing function
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
        # ✅ Lazy-load the model only when needed
        from tensorflow.keras.models import load_model
        model = load_model("b-h-1000.h5")

        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        image_file = request.files['image']
        image_data = image_file.read()

        # Optional: Save to MongoDB
        collection.insert_one({
            "filename": image_file.filename,
            "data": Binary(image_data)
        })

        # Preprocess and predict
        processed = preprocess_image(image_data)
        prediction = model.predict(processed)

        # Classify
        predicted_index = np.argmax(prediction, axis=1)[0]
        predicted_class = class_labels[predicted_index]

        return jsonify({
            "filename": image_file.filename,
            "predicted_class": predicted_class,
            "raw_output": prediction.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
