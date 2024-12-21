# README.md for Predictive Maintenance Aircraft Engine

## Overview

This project implements a predictive maintenance system for aircraft engines. It is a full-stack solution with a **frontend** built using **Dash** for visualization and a **backend** built with **Flask** for handling data and logic. The application is designed to monitor and predict the maintenance needs of aircraft engines based on sensor data, which can help prevent unexpected failures and improve operational efficiency.

The system is divided into two main components:

1. **Frontend (Dash)**: Displays real-time predictions, visualizations, and analytics to the user.
2. **Backend (Flask)**: Handles data processing, model inference, and exposes an API to interact with the frontend.

The backend communicates with the frontend to display maintenance predictions and other useful metrics. Both components will be containerized using Docker and managed with Docker Compose for ease of deployment.

## Architecture

- **Backend (Flask)**:
  - Handles requests for predictive maintenance data.
  - Implements the predictive model logic to forecast maintenance needs.
  - Exposes a REST API that the frontend communicates with.
  
- **Frontend (Dash)**:
  - Displays the predictions and data visualizations in real-time.
  - Allows the user to interact with the predictions, view trends, and analyze the data.

## Docker Setup

The application uses Docker for containerization. It includes the following services:

- **Backend**: A Flask-based API service that runs on port `5000`.
- **Frontend**: A Dash application that runs on port `8050`.

The services are connected through a custom Docker network called `app-network`.

### Docker Compose File (`docker-compose.yml`)

This file defines the services, builds, and configuration for both the frontend and backend:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    networks:
      - app-network

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "8050:8050"
    depends_on:
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

- **backend**: The Flask backend service that handles all the API requests.
- **frontend**: The Dash frontend service that communicates with the backend API to show predictions and graphs.
- **app-network**: A bridge network to enable communication between the frontend and backend services.

## Backend Dockerfile (`backend/Dockerfile`)

This Dockerfile is used to build the backend service container.

```Dockerfile
# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY backend/requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code into the container
COPY backend/ /app/

# Expose the Flask port (5000)
EXPOSE 5000

# Set the environment variable to run Flask in production mode
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask application
CMD ["flask", "run"]
```

- Installs Python dependencies from `backend/requirements.txt`.
- Copies the backend code into the container.
- Exposes port `5000` for the Flask application.
- Starts the Flask server with `flask run`.

## Frontend Dockerfile (`frontend/Dockerfile`)

This Dockerfile is used to build the frontend service container.

```Dockerfile
# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY frontend/requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application code into the container
COPY frontend/ /app/

# Expose the Dash port (8050)
EXPOSE 8050

# Run the Dash application
CMD ["python", "app.py"]
```

- Installs Python dependencies from `frontend/requirements.txt`.
- Copies the frontend code into the container.
- Exposes port `8050` for the Dash application.
- Starts the Dash server by running `app.py`.

## Running the Application

### Prerequisites

- **Docker** and **Docker Compose** must be installed on your machine.

### Steps to Run the Application

1. Clone the repository and navigate to the project directory.
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. Build and start the application using Docker Compose.
   ```bash
   docker-compose up --build
   ```

3. Once the containers are up and running, you can access the following services:
   - **Backend API**: `http://localhost:5000` (for API calls and data processing)
   - **Frontend (Dash)**: `http://localhost:8050` (for interactive visualization)

4. To stop the services, press `Ctrl+C` or run:
   ```bash
   docker-compose down
   ```

## Dependencies

The project has the following dependencies:

### Backend (`backend/requirements.txt`)

- `Flask` - For building the API.
- `pandas` - For handling data.
- `numpy` - For numerical operations.
- `scikit-learn` - For machine learning models (if any).

### Frontend (`frontend/requirements.txt`)

- `dash` - For building the web application.
- `pandas` - For handling data.
- `plotly` - For data visualization.
- `requests` - For making API calls to the backend.

## Predictive Maintenance Model

The predictive maintenance model (e.g., machine learning model) is integrated into the backend to predict when maintenance is needed based on the input data. This model could be a classification or regression model trained on historical engine sensor data. The backend will return predictions in response to frontend requests, which will then be displayed to the user.

## Conclusion

This system provides a full-stack solution for predictive maintenance in aircraft engines. The combination of Flask for backend logic and Dash for frontend visualization ensures an efficient and user-friendly experience for monitoring engine performance and predicting maintenance requirements. With Docker and Docker Compose, the application can be easily deployed and scaled.
