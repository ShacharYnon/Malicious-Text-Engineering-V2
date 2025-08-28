import os
from typing import List

KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092").split(",")
KAFKA_TOPIC_ANTI = os.getenv("KAFKA_TOPIC_ANTI" ,"enriched_preprocessed_tweets_antisemitic")
KAFKA_TOPIC_NOT_ANTI = os.getenv("KAFKA_TOPIC_NOT_ANTI" ,"enriched_preprocessed_tweets_not_antisemitic")

