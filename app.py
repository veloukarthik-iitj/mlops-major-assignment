# app.py
"""
Simple Flask app to upload an image and predict Olivetti face class using a saved DecisionTreeClassifier.
Assumes models/savedmodel.pth exists in the container (image should include it via Docker build or mount).
"""
import os
import joblib
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
MODEL_PATH = os.path.join('models', 'savedmodel.pth')
_model = None

def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"{MODEL_PATH} not found in container.")
        data = joblib.load(MODEL_PATH)
        _model = data['model']
    return _model

def preprocess_image(file_storage):
    """
    Convert input image to 64x64 grayscale and scale similarly to Olivetti dataset (0..1).
    Returns a 2D array shaped (1, 4096)
    """
    img = Image.open(file_storage).convert('L').resize((64, 64))
    arr = np.asarray(img, dtype=np.float32).reshape(1, -1)
    arr = arr / 255.0
    return arr

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if not file:
        return redirect(url_for('index'))
    X = preprocess_image(file)
    clf = load_model()
    pred = clf.predict(X)[0]
    return render_template('upload.html', result=pred)

if __name__ == '__main__':
    # For local debug only. In Docker/K8s use a production server like gunicorn.
    app.run(host='0.0.0.0', port=5001)
