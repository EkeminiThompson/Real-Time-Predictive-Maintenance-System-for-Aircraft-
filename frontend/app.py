# -*- coding: utf-8 -*-
# app.py - Dash Application for Real-Time Predictive Maintenance Dashboard

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import random
import pandas as pd
import json
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Predictive Maintenance Dashboard", style={'textAlign': 'center'}),
    
    # Real-time sensor data display
    html.Div([
        html.Div([
            html.H3("Vibration (g)", style={'margin': '10px'}),
            html.Div(id="vibration-value", style={'fontSize': '2rem', 'color': 'blue'})
        ], className="sensor-panel"),

        html.Div([
            html.H3("Temperature (°C)", style={'margin': '10px'}),
            html.Div(id="temperature-value", style={'fontSize': '2rem', 'color': 'green'})
        ], className="sensor-panel"),

        html.Div([
            html.H3("Pressure (psi)", style={'margin': '10px'}),
            html.Div(id="pressure-value", style={'fontSize': '2rem', 'color': 'red'})
        ], className="sensor-panel"),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),

    # Graph for Real-time Data
    dcc.Graph(id="real-time-graph"),

    # Maintenance Prediction Status
    html.Div(id="prediction-result", style={'fontSize': '1.5rem', 'color': 'red', 'textAlign': 'center'})
])

# Function to fetch sensor data from Flask API
def fetch_sensor_data():
    try:
        response = requests.get("http://127.0.0.1:5000/sensor-data")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching sensor data: {e}")
        return {}

# Function to fetch maintenance prediction
def fetch_prediction(data):
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=data)
        prediction = response.json()
        return prediction['maintenance_needed']
    except Exception as e:
        print(f"Error fetching prediction: {e}")
        return None

# Callback to update sensor data and prediction
@app.callback(
    [Output('vibration-value', 'children'),
     Output('temperature-value', 'children'),
     Output('pressure-value', 'children'),
     Output('real-time-graph', 'figure'),
     Output('prediction-result', 'children')],
    [Input('real-time-graph', 'relayoutData')]
)
def update_dashboard(_):
    # Fetch real-time sensor data
    sensor_data = fetch_sensor_data()
    
    # If data is not available, return placeholders
    if not sensor_data:
        return ("N/A", "N/A", "N/A", {}, "Error fetching data")
    
    vibration = sensor_data.get('vibration', "N/A")
    temperature = sensor_data.get('temperature', "N/A")
    pressure = sensor_data.get('pressure', "N/A")

    # Prepare the prediction data
    prediction_data = {
        'mean_vibration': vibration,
        'std_vibration': random.uniform(0.05, 0.1),  # Fake std_vibration for now
        'temp_difference': random.uniform(0.5, 1.5),  # Fake temp_difference
        'pressure_diff': random.uniform(0.5, 1.0)  # Fake pressure_diff
    }

    # Get maintenance prediction
    maintenance_needed = fetch_prediction(prediction_data)

    # Update the graph with real-time data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[time.time()], y=[vibration], mode='lines+markers', name='Vibration'))
    fig.add_trace(go.Scatter(x=[time.time()], y=[temperature], mode='lines+markers', name='Temperature'))
    fig.add_trace(go.Scatter(x=[time.time()], y=[pressure], mode='lines+markers', name='Pressure'))

    # Show the result of the maintenance prediction
    if maintenance_needed:
        prediction_result = "🚨 Maintenance Needed! ⚠️"
    else:
        prediction_result = "✅ No Maintenance Needed."

    return (
        f"{vibration:.2f}", f"{temperature:.2f}", f"{pressure:.2f}",
        fig, prediction_result
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
