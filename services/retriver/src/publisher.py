import logging
from .. import config
import json
from typing import List
from kafka import KafkaProducer

logger = logging.getLogger(__name__)

class Publisher:
    """"
    a Kafka Publisher to send messages to a topic
    """
    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info(f"Kafka Producer initialized with bootstrap servers: {config.KAFKA_BOOTSTRAP}")
    
    def publish(self, topic: str, message: List[dict]):
        """
        Publish a message to a Kafka topic
        
        Args:
            topic (str): Kafka topic name
            message (dict): Message to send
        """
        try:
            for m in message:
                self._producer.send(topic, value=m)
            self._producer.flush()
            logger.info(f"Message published to topic '{topic}': {message}")
        except Exception as e:
            logger.error(f"Failed to publish message to topic '{topic}': {e}")
            raise RuntimeError(f"Failed to publish message to topic '{topic}': {e}")