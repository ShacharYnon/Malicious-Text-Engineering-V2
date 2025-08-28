from typing import Iterable, List, Dict, Any, Optional
from kafka import KafkaConsumer
from bson import json_util
import logging

logger = logging.getLogger(__name__)


class Consumer:
    """
    Lightweight Kafka consumer that yields each message's value (a dict).
    """

    def __init__(self, topics: List[str], kafka_bootstrap: List[str], group_id: str):
        """
        :param topics: list of topic names to subscribe to
        :param kafka_bootstrap: list of bootstrap server addresses
        :param group_id: consumer group id
        """
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=kafka_bootstrap,
            value_deserializer=lambda m: json_util.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=group_id,
        )

        logger.info(
            f"KafkaConsumer created. topics={topics}, bootstrap={kafka_bootstrap}, group_id={group_id}"
        )

    def consume_messages(self) -> Iterable[Dict[str, Any]]:
        """
        Yield each message value as a dict.
        """
        try:
            for message in self.consumer:
                val = message.value
                if not isinstance(val, dict):
                    logger.warning(
                        f"Expected dict payload but got {type(val).__name__}; wrapping into dict."
                    )
                    val = {"payload": val}
                logger.debug(f"Consumed from {message.topic}@{message.partition}/{message.offset}")
                yield val
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            raise RuntimeError(f"Error consuming messages: {e}")

    def close(self) -> None:
        try:
            self.consumer.close()
        finally:
            logger.info("Kafka consumer closed.")
