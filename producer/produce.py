from confluent_kafka import Producer
import json
import time
import random

# Kafka configuration
conf = {
    'bootstrap.servers': 'kafka:9092'  # The service name and port defined in docker-compose.yml
}

# Create the Kafka Producer
producer = Producer(**conf)

# Sample data for event simulation
users = ['user_1', 'user_2', 'user_3']
songs = ['song_1', 'song_2', 'song_3', 'song_4']
actions = ['play', 'like', 'add_to_playlist']

def generate_event():
    """Generates a random music event"""
    user = random.choice(users)
    song = random.choice(songs)
    action = random.choice(actions)
    timestamp = int(time.time())
    
    # Create a simple event structure
    event = {
        'user_id': user,
        'song_id': song,
        'action': action,
        'timestamp': timestamp
    }
    
    return json.dumps(event)

def delivery_report(err, msg):
    """Called once for each message produced to confirm delivery"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def main():
    while True:
        # Generate a random event
        event = generate_event()
        
        # Send the event to Kafka topic (e.g., "song_plays")
        producer.produce('song_plays', event, callback=delivery_report)
        
        # Poll to ensure delivery
        producer.poll(1)
        
        # Sleep to simulate real-time event generation
        time.sleep(2)  # Generate an event every 2 seconds

if __name__ == '__main__':
    main()