from kafka import KafkaConsumer
from .. import config
import logging
logger = logging.getLogger(__name__)

class Consumer:
    
    def __init__(self):

        self.consumer = KafkaConsumer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        self.consumer.subscribe(topics=[config.KAFKA_TOPIC_ANTI,config.KAFKA_TOPIC_NOT_ANTI])
        for message in self.consumer:
            print(f"Received message: {message.value.decode('utf-8')} from topic: {message.topic}")