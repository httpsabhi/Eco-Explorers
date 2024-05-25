from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from predict import MakePrediction
from flask_cors import CORS
import os
import tensorflow as tf

app = Flask(__name__)
CORS(app)

app.animal_model = load_model('models/animal.keras')

def predict(model, classes):
    image = request.files.get('image')
    if not image:
        return "No image found", 0
    else:
        # Define the upload folder and ensure it exists
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Save the uploaded image to the server
        image_filename = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_filename)
        return MakePrediction(image_filename, model, classes)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        classes = ['cheetah', 'fox', 'hyena', 'lion', 'tiger', 'wolf']
        result = predict(app.animal_model, classes)
        return jsonify(result=result)
    else:
        return jsonify(result=("Server Error", 0))

if __name__ == '__main__':
    app.run(debug=True)
