# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies required for PIL and PyTorch
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install the required packages
RUN pip install --no-cache-dir flask torch torchvision pillow requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Use an environment variable to specify the script to run
ENV PYTHON_SCRIPT app.py

# Run the specified Python script when the container launches
CMD ["sh", "-c", "python ${PYTHON_SCRIPT}"]