# Use a slim Python 3.9 image as the base
FROM python:3.9-slim

# Install system dependencies for confluent-kafka and cassandra-driver
RUN apt-get update && apt-get install -y \
    gcc \
    librdkafka-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the correct permissions
RUN chmod +x consume.py

# Default command to run the consumer script
CMD ["python", "consume.py"]