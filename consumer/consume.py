from confluent_kafka import Consumer, KafkaException
from cassandra.cluster import Cluster
import json 

# Kafka configuration
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'music-consumers',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Start from earliest messages in the topic
}

# Create a Kafka consumer
consumer = Consumer(**conf)
consumer.subscribe(['song_plays'])  # Subscribe to the 'song_plays' topic

# Set up Cassandra connection
cluster = Cluster(['cassandra'])  # 'cassandra' is the service name in Docker
session = cluster.connect()

# Create Cassandra table if it doesn't exist
session.execute("""
CREATE KEYSPACE IF NOT EXISTS music_streaming WITH REPLICATION = {
    'class': 'SimpleStrategy', 'replication_factor': 1
};
""")

session.execute("""
CREATE TABLE IF NOT EXISTS music_streaming.song_activity (
    user_id text,
    song_id text,
    action text,
    timestamp bigint,
    PRIMARY KEY (song_id, timestamp)
);
""")

def store_event_in_cassandra(event):
    """Insert event data into Cassandra table"""
    query = """
    INSERT INTO music_streaming.song_activity (user_id, song_id, action, timestamp)
    VALUES (%s, %s, %s, %s)
    """
    session.execute(query, (event['user_id'], event['song_id'], event['action'], event['timestamp']))

def main():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    print(f"Reached end of partition at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                # Process message
                event = json.loads(msg.value().decode('utf-8'))
                print(f"Received event: {event}")

                # Store the event in Cassandra
                store_event_in_cassandra(event)
                
    except KeyboardInterrupt:
        print("Stopping consumer.")
    finally:
        consumer.close()

if __name__ == '__main__':
    main()