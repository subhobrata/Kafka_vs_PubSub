import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import MagicMock, patch
from src import messaging


def test_produce_kafka_message():
    with patch('src.messaging.Producer') as MockProducer:
        producer_instance = MockProducer.return_value
        messaging.produce_kafka_message('broker', 'topic', 'msg')
        producer_instance.produce.assert_called_once_with('topic', b'msg')
        producer_instance.flush.assert_called_once()


def test_consume_kafka_messages():
    with patch('src.messaging.Consumer') as MockConsumer:
        mock_consumer = MockConsumer.return_value
        msg = MagicMock()
        msg.error.return_value = None
        msg.value.return_value = b'msg'
        # Return message then None to stop loop
        mock_consumer.poll.side_effect = [msg]
        messages = messaging.consume_kafka_messages('broker', 'topic', 'group')
        assert messages == ['msg']
        mock_consumer.close.assert_called_once()


def test_publish_pubsub_message():
    with patch('src.messaging.pubsub_v1.PublisherClient') as MockPublisher:
        publisher = MockPublisher.return_value
        future = MagicMock()
        future.result.return_value = 'id1'
        publisher.publish.return_value = future
        msg_id = messaging.publish_pubsub_message('pid', 'topic', 'hello')
        publisher.topic_path.assert_called_once_with('pid', 'topic')
        publisher.publish.assert_called_once()
        assert msg_id == 'id1'


def test_subscribe_pubsub_messages():
    with patch('src.messaging.pubsub_v1.SubscriberClient') as MockSub:
        subscriber = MockSub.return_value
        future = MagicMock()
        future.result.side_effect = Exception('stop')
        subscriber.subscribe.return_value = future
        try:
            messaging.subscribe_pubsub_messages('pid', 'sub', lambda m: None, timeout=0.1)
        except Exception:
            pass
        subscriber.subscription_path.assert_called_once_with('pid', 'sub')
        subscriber.subscribe.assert_called_once()
        future.cancel.assert_called_once()
