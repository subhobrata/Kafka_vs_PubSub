from typing import List, Callable

# Kafka imports
from confluent_kafka import Producer, Consumer

# Pub/Sub imports
from google.cloud import pubsub_v1


def produce_kafka_message(broker: str, topic: str, message: str) -> None:
    """Publish a message to a Kafka topic."""
    producer = Producer({"bootstrap.servers": broker})
    producer.produce(topic, message.encode("utf-8"))
    producer.flush()


def consume_kafka_messages(
    broker: str,
    topic: str,
    group_id: str,
    *,
    max_messages: int = 1,
    timeout: float = 1.0,
) -> List[str]:
    """Consume messages from a Kafka topic and return them as strings."""
    consumer = Consumer(
        {
            "bootstrap.servers": broker,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([topic])

    messages = []
    while len(messages) < max_messages:
        msg = consumer.poll(timeout)
        if msg is None:
            continue
        if msg.error():
            raise RuntimeError(msg.error())
        messages.append(msg.value().decode("utf-8"))

    consumer.close()
    return messages


def publish_pubsub_message(project_id: str, topic_id: str, message: str) -> str:
    """Publish a message to a Google Cloud Pub/Sub topic and return the message ID."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, message.encode("utf-8"))
    return future.result()


def subscribe_pubsub_messages(
    project_id: str,
    subscription_id: str,
    callback: Callable[[pubsub_v1.subscriber.message.Message], None],
    *,
    timeout: float | None = None,
) -> None:
    """Subscribe to a Pub/Sub subscription and process messages via callback."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    streaming_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_future.result(timeout=timeout)
    except Exception:
        streaming_future.cancel()
        raise

