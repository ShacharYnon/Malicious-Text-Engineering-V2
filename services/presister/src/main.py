from pydoc_data import topics
from dal import MongoDAL
from .. import config
import logging
from ...utils.consumer import Consumer
import json

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class PresisterService:
    def __init__(self):
        self.dal = MongoDAL(
            uri=config.MONGO_URI,
            db_name=config.MONGO_DB,
            coll_antisemitic=config.MONGODB_COL_ANTISEMITIC,
            coll_not_antisemitic=config.MONGODB_COL_NOT_ANTISEMITIC,
        )
        self.consumer = Consumer(
            topics=config.TOPICS_ENRICHER,          
            kafka_bootstrap=config.KAFKA_BOOTSTRAP,
            group_id="presister_group",
        )

    def persist_antisemitic(self, docs):
        count = self.dal.insert_antisemitic(docs)
        logger.info(f"Persisted {count} antisemitic documents.")

    def persist_not_antisemitic(self, docs):
        count = self.dal.insert_not_antisemitic(docs)
        logger.info(f"Persisted {count} not antisemitic documents.")

    def process_message(self, message):
        try:
            data = json.loads(message.value.decode('utf-8'))
            prediction = data.get('prediction')
            documents = data.get('documents', [])
            
            if prediction == 'antisemitic':
                self.persist_antisemitic(documents)
            elif prediction == 'not_antisemitic':
                self.persist_not_antisemitic(documents)
            else:
                logger.warning(f"Unknown prediction type: {prediction}")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def start(self):
        logger.info("Starting Presister Service...")
        try:
            for message in self.consumer.consume_messages():
                self.process_message(message)
        except KeyboardInterrupt:
            logger.info("Shutting down Presister Service...")
        finally:
            self.consumer.close()

    def stop(self):
        self.consumer.close()
        logger.info("Presister Service stopped.")


if __name__ == "__main__":
    service = PresisterService()
    service.start()