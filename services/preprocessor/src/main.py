import logging
import time
from typing import List, Dict, Any

from utils.data_processor import TextCleaner
from utils.consumer import Consumer
from utils.publisher import Publisher

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class ProcessManager:
    """
    Consume RAW_* topics, clean/transform, and publish to PROCESSED_* topics.
    """

    def __init__(
        self,
        kafka_bootstrap: List[str],
        raw_topics: List[str],
        processed_topic_anti: str,
        processed_topic_not_anti: str,
        group_id: str = "preprocessor",
        sleep_seconds: int = 10,
    ):
        self.cleaner = TextCleaner(lang="en")
        self.consumer = Consumer(
            topics=raw_topics,           # CHANGE: consume ONLY from RAW_* topics.
            kafka_bootstrap=kafka_bootstrap,
            group_id=group_id,
        )
        self.publisher = Publisher(kafka_bootstrap=kafka_bootstrap)
        self.topic_anti = processed_topic_anti
        self.topic_not_anti = processed_topic_not_anti
        self.sleep_seconds = sleep_seconds

        logger.info(
            f"ProcessManager ready. raw_topics={raw_topics}, "
            f"processed_anti={processed_topic_anti}, processed_not_anti={processed_topic_not_anti}"
        )

    def _process_one(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        text = doc.get("text") or doc.get("Text") or ""
        doc["Cleaned_Text"] = self.cleaner.clean_central(text)
        return doc

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
                        processed = self._process_one(doc)
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


# if __name__ == "__main__":
#     BOOTSTRAP = ["localhost:9092"]
#     RAW_TOPICS = ["RAW_TWEETS"]
#     PROCESSED_ANTI = "PROCESSED_ANTI"
#     PROCESSED_NOT_ANTI = "PROCESSED_NOT_ANTI"

#     mgr = ProcessManager(
#         kafka_bootstrap=BOOTSTRAP,
#         raw_topics=RAW_TOPICS,
#         processed_topic_anti=PROCESSED_ANTI,
#         processed_topic_not_anti=PROCESSED_NOT_ANTI,
#         group_id="preprocessor",
#         sleep_seconds=10,
#     )
#     mgr.run_forever()
