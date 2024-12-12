import time
import json
import random

from confluent_kafka import Consumer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

from loguru import logger as log
from pathlib import Path
from uuid import uuid4


consumer = Consumer({
    "group.id": "music_streaming_data",
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


def main():
    """
    Main function to consume messages from the Kafka topic 'music_streaming_data',
    sanitize the JSON messages, and log the sanitized data.
    """
    topic_name = "music_streaming_data"

    consumer.subscribe([topic_name])
    results = []
    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                log.error(f"Consumer error: {message.error()}")

            message = message.value().decode('unicode_escape')
            # How the heck is it this hard to convert the
            # message to a dictionary?
            # message = json.loads(message) # throwing decoding error...
            log.info(f"Consumed message:\n{message}")
    except KeyboardInterrupt:
        log.info("Stopping kafka consumer")
        consumer.close()

    consumer.close()
    return results

if __name__ == "__main__":
    main()
