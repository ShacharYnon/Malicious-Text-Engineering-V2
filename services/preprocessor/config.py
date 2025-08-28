import os
from typing import List

KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP", "localhost:9094").split(",")
KAFKA_TOPIC_ANTI = os.getenv("KAFKA_TOPIC_ANTI" ,"preprocessed_tweets_antisemitic")
KAFKA_TOPIC_NOT_ANTI = os.getenv("KAFKA_TOPIC_NOT_ANTI" ,"preprocessed_tweets_not_antisemitic")

GROUP_ID = os.getenv("GROUP_ID" ,"preprocessur_group")

RAW_TOPICS: List[str] = os.getenv("RAW_TWEETS" , ["raw_tweets_antisemitic", "raw_tweets_not_antisemitic"])

# Topics from retriver 
# KAFKA_TOPIC_ANTI = "raw_tweets_antisemitic")
# KAFKA_TOPIC_NOT_ANTI = "raw_tweets_not_antisemitic")