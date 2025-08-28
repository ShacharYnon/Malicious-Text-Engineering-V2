from typing import Iterable, Dict, Any, List
from kafka import KafkaProducer
from bson import json_util
import logging

logger = logging.getLogger(__name__)


class Publisher:
    """
    Kafka Publisher to send messages to a topic.
    """

    def __init__(self, kafka_bootstrap: List[str]):
        self._producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap,
            value_serializer=lambda v: json_util.dumps(v).encode("utf-8"),
        )
        logger.info(f"KafkaProducer created. bootstrap={kafka_bootstrap}")

    def publish(self, topic: str, messages: Iterable[Dict[str, Any]]) -> None:
        """
        Publish an iterable of dict messages to `topic`.
        """
        # CHANGE: clarified type to iterable-of-dicts; producer sends each item separately.
        try:
            count = 0
            for m in messages:
                self._producer.send(topic, value=m)
                count += 1
            self._producer.flush()
            logger.info(f"Published {count} message(s) to topic '{topic}'.")
        except Exception as e:
            logger.error(f"Failed to publish to '{topic}': {e}")
            raise RuntimeError(f"Failed to publish to '{topic}': {e}")

    def publish_one(self, topic: str, message: Dict[str, Any]) -> None:
        self.publish(topic, [message])

    def close(self) -> None:
        """
        Close the Kafka producer.
        """
        try:
            self._producer.flush()
            self._producer.close()
        finally:
            logger.info("Kafka producer closed.")
