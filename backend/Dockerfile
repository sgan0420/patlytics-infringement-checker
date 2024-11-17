# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt ./

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Define the command to run your Flask app
CMD ["python", "app.py"]
