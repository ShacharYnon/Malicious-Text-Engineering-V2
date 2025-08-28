import os
from typing import List

MONGODB_URI = os.getenv("MONGODB_URI" ,"mongodb+srv://IRGC_NEW:iran135@cluster0.6ycjkak.mongodb.net/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE" ,"IranMalDB")
MONGODB_COL = os.getenv("MONGODB_COL" ,"tweets")

KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP", "localhost:9094").split(",")
KAFKA_TOPIC_ANTI = os.getenv("KAFKA_TOPIC_ANTI" ,"raw_tweets_antisemitic")
KAFKA_TOPIC_NOT_ANTI = os.getenv("KAFKA_TOPIC_NOT_ANTI" ,"raw_tweets_not_antisemitic")





