# app.py - Flask API to serve the Predictive Maintenance Model

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for development

# Load the pre-trained predictive model (Random Forest)
model = joblib.load('predictive_model.pkl')  # Make sure to train the model first

# Simulate sensor data for demonstration purposes
def generate_fake_data():
    """
    Function to generate synthetic sensor data for the aircraft.
    This will be replaced by real sensor data in a production system.
    """
    return {
        'timestamp': datetime.now().isoformat(),
        'vibration': random.uniform(0.4, 0.8),  # Vibration data
        'temperature': random.uniform(50, 100),  # Temperature data
        'pressure': random.uniform(25, 35),  # Pressure data
    }

@app.route('/')
def home():
    return "Predictive Maintenance API for Aircraft - Ready!"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to predict if maintenance is required based on sensor data features.
    """
    data = request.get_json()  # Extract input JSON data
    
    # Prepare features from the incoming data
    features = np.array([
        data['mean_vibration'],
        data['std_vibration'],
        data['temp_difference'],
        data['pressure_diff']
    ]).reshape(1, -1)

    # Predict if maintenance is needed
    prediction = model.predict(features)

    # Return the prediction result
    response = {
        'maintenance_needed': bool(prediction[0])  # Convert to boolean
    }
    return jsonify(response)

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    """
    Endpoint to fetch simulated sensor data for the dashboard.
    """
    data = generate_fake_data()  # Generate fake sensor data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in development mode
