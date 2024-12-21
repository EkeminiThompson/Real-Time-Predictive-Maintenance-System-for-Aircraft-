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
