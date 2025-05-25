from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Upload folder setup
UPLOAD_FOLDER = 'uploads'
if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    logging.warning(f"'{UPLOAD_FOLDER}' exists and is not a directory. Removing it.")
    os.remove(UPLOAD_FOLDER)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# MongoDB connection
try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.get_default_database()  # This will be 'image_analysis' from URI
    collection = db['results']
except Exception as e:
    logging.error("MongoDB connection failed: %s", str(e))

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({'error': 'Invalid filename'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Dummy analysis result
    result = {"filename": filename, "message": "Analysis complete!"}

    try:
        collection.insert_one(result)
    except Exception as e:
        return jsonify({'error': 'Failed to save to DB', 'details': str(e)}), 500

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
