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
    topic_name = "music_streaming_data"

    consumer.subscribe([topic_name])
    data = {}
    try:
        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                log.error(f"Consumer error: {message.error()}")
                continue
            data = json.loads(message.value())
            break
    except KeyboardInterrupt:
        log.info("Stopping data consumption.")
    finally:
        consumer.close()
    return data

if __name__ == "__main__":
    main()
