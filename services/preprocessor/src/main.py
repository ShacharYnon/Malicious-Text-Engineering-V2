from .. import config
import logging
from ...utils.data_processor import TextCleaner
from ...utils.consumer import Consumer
from ...utils.publisher import Publisher
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class ProcessManager:
    def __init__(self):
        self.publisher = Publisher(config.KAFKA_BOOTSTRAP)
        self.topic_anti = config.KAFKA_TOPIC_ANTI
        self.topic_not_anti = config.KAFKA_TOPIC_NOT_ANTI
        self.data = None
        self.processor = TextCleaner()
    
    def process_and_publish(self):
        logger.info("Starting message consumption and processing")
        consumer = Consumer([self.topic_anti ,self.topic_not_anti] ,config.KAFKA_BOOTSTRAP ,config.GROUP_ID) 
        for message in consumer.consume_messages():
            processed_anti = []
            processed_not_anti = []
            # for doc in message:
            try:
                cleaned_text = self.processor.clean_central(message.get("text", ""))
                message["Cleaned_Text"] = cleaned_text
                if message.get("Antisemitic", False):
                    processed_anti.append(message)
                else:
                    processed_not_anti.append(message)
            except Exception as e:
                    logger.error(f"Error processing document ID {message.get('_id')}: {e}")
            if processed_anti:
                self.publisher.publish(self.topic_anti, processed_anti)
            if processed_not_anti:
                self.publisher.publish(self.topic_not_anti, processed_not_anti)
            logger.info(f"Processed and published {len(processed_anti)} antisemitic and {len(processed_not_anti)} non-antisemitic documents")

    def main(self):
        self.process_and_publish()


if __name__ == "__main__":
    manager = ProcessManager()
    manager.process_and_publish()

# 