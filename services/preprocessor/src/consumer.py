from kafka import KafkaConsumer
import json
import logging
from typing import List
from .. import config 
logger = logging.getLogger(__name__)

class Consumer:
    def __init__(self, topic: str, bootstrap_servers: List[str]):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            # group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        logger.info(f"Kafka consumer initialized for topic: {topic}")

    def consume_messages(self):
        """"
        Consume messages from the Kafka topic
        Yields:
            message (Dict): The consumed message
        """
        try:
            for message in self.consumer:
                logger.info(f"Consumed message: {message.value}")
                yield message.value
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            raise RuntimeError(f"Error consuming messages: {e}")



# if __name__ == "__main__":    
#     cons = Consumer(
#         topic=config.KAFKA_TOPIC_NOT_ANTY,
#         bootstrap_servers=["127.0.0.1:9094"],
#     )
#     for msg in cons.consume_messages():
#         print(msg)