import os
from typing import List

KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092").split(",")
KAFKA_TOPIC_ANTI = os.getenv("KAFKA_TOPIC_ANTI" ,"raw_tweets_antisemitic")
KAFKA_TOPIC_NOT_ANTY = os.getenv("KAFKA_TOPIC_NOT_ANTY" ,"raw_tweets_not_antisemitic")