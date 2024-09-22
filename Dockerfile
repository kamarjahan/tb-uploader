# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the container’s entry point is the bot’s script
CMD ["python", "main.py"]
