# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory (your Flask app and the csv folder) into the container's /app directory
COPY . /app

# Install the required Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Flask default port (5000)
EXPOSE 5000

# Set the environment variable to ensure Flask runs in development mode
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the Flask application
CMD ["flask", "run", "--debug", "--host=0.0.0.0"]
