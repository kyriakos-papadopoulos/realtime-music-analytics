# Use a slim Python 3.9 image as the base
FROM python:3.9-slim

# Install system dependencies, including gcc, librdkafka, and any necessary libraries for building confluent-kafka
RUN apt-get update && apt-get install -y \
    gcc \
    librdkafka-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the Python script (adjust based on whether it's producer or consumer)
CMD ["python", "produce.py"]  # For producer