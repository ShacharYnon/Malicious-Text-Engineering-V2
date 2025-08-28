import os
from typing import List

KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP", "localhost:9094").split(",")
KAFKA_TOPIC_ANTI = os.getenv("KAFKA_TOPIC_ANTI" ,"enriched_preprocessed_tweets_antisemitic")
KAFKA_TOPIC_NOT_ANTI = os.getenv("KAFKA_TOPIC_NOT_ANTI" ,"enriched_preprocessed_tweets_not_antisemitic")

TOPICS_PREPROCESSOR: List[str] = os.getenv("TOPICS_PREPROCESSOR" , ["preprocessed_tweets_antisemitic", "preprocessed_tweets_not_antisemitic"])

# KAFKA_TOPIC_ANTI = "preprocessed_tweets_antisemitic"
# KAFKA_TOPIC_NOT_ANTI = "preprocessed_tweets_not_antisemitic"