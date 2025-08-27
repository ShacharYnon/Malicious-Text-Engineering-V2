import os
from typing import List

MONGODB_URI = os.getenv("MONGODB_URI" ,"mongodb+srv://IRGC_NEW:iran135@cluster0.6ycjkak.mongodb.net/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE" ,"IranMalDB")
MONGODB_COL = os.getenv("MONGODB_COL" ,"tweets")
KAFKA_BOOTSTRAP: List[str] = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092").split(",")






