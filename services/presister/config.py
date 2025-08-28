import os
from typing import List
##test config file

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "mydatabase")

MONGODB_COL_ANTISEMITIC = os.getenv("MONGODB_COL_ANTISEMITIC", "antisemitic_collection")
MONGODB_COL_NOT_ANTISEMITIC = os.getenv("MONGODB_COL_NOT_ANTISEMITIC", "not_antisemitic_collection")

KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")

TOPICS_ENRICHER: List[str] = os.getenv("TOPICS_ENRICHER", "enriched_preprocessed_tweets_antisemitic,enriched_preprocessed_tweets_not_antisemitic").split(",")

# TOPIC_ANT = "enriched_preprocessed_tweets_antisemitic"
# TOPIC_NOT_ANT = "enriched_preprocessed_tweets_not_antisemitic"

