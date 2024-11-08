import time
import json
import random

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

from loguru import logger as log
from pathlib import Path
from uuid import uuid4


# Constants
SLEEP_TIME = 3 # Adjust to send streaming events more or less frequently
STREAMING_SONGS_FILE = "streaming-songs.json"
STREAMING_USERS_FILE = "streaming-users.json"

producer = Producer({
    "bootstrap.servers": "127.0.0.1:9092",
})

def delivery_report(err, msg) -> None:
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush().
    """
    if err is not None:
        log.warning(f"Message delivery failed: {err}")
        return None
    log.warning(f"Message delivered to: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()}")


def get_json_data_from_file(file_path: str) -> dict:
    """Read JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)
    return {}


def main():
    topic_name = "music_streaming_data"

    # Load streaming songs and users
    current_dir = Path(__file__).resolve().parent
    streaming_songs_path = current_dir / STREAMING_SONGS_FILE
    streaming_users_path = current_dir / STREAMING_USERS_FILE

    streaming_songs = get_json_data_from_file(streaming_songs_path)
    streaming_song_ids = list(streaming_songs.keys())
    streaming_users = get_json_data_from_file(streaming_users_path)

    # Load schema for music streaming data
    schema_path = current_dir / "kafka-schema.json"
    with open(schema_path, "r") as file:
        schema_str = file.read()
    schema_registry_conf = {'url': "http://127.0.0.1:8081"}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(schema_str, schema_registry_client)

    try:
        while True:
            # Serve on_delivery callbacks from previous calls to produce()
            producer.poll(0.0)
            event_count = 0
            log.info(f"Sending streaming events for {len(streaming_users)} users...")
            for key, user in streaming_users.items():
                song = streaming_songs[random.choice(streaming_song_ids)]
                music_data = {**user, **song} # Merge user and song data
                producer.produce(
                    topic=topic_name,
                    key=string_serializer(str(uuid4())),
                    value=json_serializer(music_data, SerializationContext(topic_name, MessageField.VALUE)),
                    on_delivery=delivery_report
                )
                event_count += 1

            log.info(f"Sent {event_count} music streaming events")
            # Wait for 3 seconds to send more events
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print("Stopping data generation.")
    finally:
        log.info("Flushing records...")
        producer.flush()

if __name__ == "__main__":
    main()
