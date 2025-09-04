from .features import SentimentEnhancer
from .weapons_detector import WeaponsDetector
from .. import config
import logging
import os
import time
from ...utils.consumer import Consumer
from ...utils.publisher import Publisher
from typing import List, Dict, Any
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class EnricherManager:

    def __init__(
        self,
        kafka_bootstrap: List[str],
        raw_topics: List[str],
        processed_topic_anti: str,
        processed_topic_not_anti: str,
        group_id: str = "enricher",
        sleep_seconds: int = 10,
    ):
        self.consumer = Consumer(
            topics=raw_topics,           # CHANGE: consume ONLY from RAW_* topics.
            kafka_bootstrap=kafka_bootstrap,
            group_id=group_id,
        )
        self.publisher = Publisher(kafka_bootstrap=kafka_bootstrap)
        self.topic_anti = processed_topic_anti
        self.topic_not_anti = processed_topic_not_anti
        self.sleep_seconds = sleep_seconds

        self.sentiment_enhancer = SentimentEnhancer()
        weapons_list = self._load_weapons()
        self.weapons_detector = WeaponsDetector(weapons_list)

    def _load_weapons(self)->List[str]:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        weapons_file_path = os.path.join(BASE_DIR, "..", "..", "..", "data", "weapon_list.txt")
        list_weapons = []
        try:
            with open(weapons_file_path, 'r') as file:
                list_weapons = [line.strip() for line in file if line.strip()]
            logger.info(f"Loaded {len(list_weapons)} weapons from {weapons_file_path}")
            return list_weapons
        except Exception as e:
            logger.error(f"Error loading weapons list: {e}")
            raise RuntimeError(f"Error loading weapons list: {e}")

    def enrich(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich documents with sentiment analysis and weapons detection

        Args:
            documents (List[Dict[str, Any]]): List of documents to enrich

        Returns:
            List[Dict[str, Any]]: List of enriched documents
        """
        try:
            # First apply sentiment analysis
            sentiment_enriched_docs = self.sentiment_enhancer.enrich_documents(documents)
            # Then apply weapons detection
            fully_enriched_docs = self.weapons_detector.detect_weapons(sentiment_enriched_docs)
            return fully_enriched_docs
        except Exception as e:
            logger.error(f"Error enriching documents: {e}")
            raise RuntimeError(f"Error enriching documents: {e}")
        
    def run_forever(self) -> None:
        """
        Main loop: read one-by-one, route by Antisemitic flag, publish to processed topics.
        """
        try:
            while True:
                published_anti = 0
                published_not = 0

                for doc in self.consumer.consume_messages():
                    try:
                        processed = self.sentiment_enhancer.enrich_documents(doc)
                        if processed.get("Antisemitic", False):
                            self.publisher.publish_one(self.topic_anti, processed)
                            published_anti += 1
                        else:
                            self.publisher.publish_one(self.topic_not_anti, processed)
                            published_not += 1
                    except Exception as e:
                        logger.exception(f"Failed processing document id={doc.get('_id')}: {e}")

                logger.info(
                    f"Cycle done. Published anti={published_anti}, not_anti={published_not}. "
                    f"Sleeping {self.sleep_seconds}s."
                )
                time.sleep(self.sleep_seconds)
        finally:
            self.consumer.close()
            self.publisher.close()
        


        
    
if __name__ == "__main__":
    # sample_docs = [
    #     {"_id": 1, "Cleaned_Text": "This is a test text with a gun."},
    #     {"_id": 2, "Cleaned_Text": "No weapons here."},
    #     {"_id": 3, "Cleaned_Text": "Another text with a knife and a rifle."}
    # ]
    enricher = EnricherManager(
        kafka_bootstrap=config.KAFKA_BOOTSTRAP,
        raw_topics=config.TOPICS_PREPROCESSOR,
        processed_topic_anti=config.KAFKA_TOPIC_ANTI,
        processed_topic_not_anti=config.KAFKA_TOPIC_NOT_ANTI,
        group_id="preprocessor"
        # sleep_seconds=10,
    )
    enricher.run_forever()
    
    enriched_docs = enricher.enrich(config.TOPICS_PREPROCESSOR)
    for doc in enriched_docs:
        print(doc)


#
# python -m services.enricher.src.main