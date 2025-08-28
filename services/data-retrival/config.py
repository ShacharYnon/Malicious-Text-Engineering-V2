import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "mydatabase")

MONGODB_COL_ANTISEMITIC = os.getenv("MONGODB_COL_ANTISEMITIC", "antisemitic_collection")
MONGODB_COL_NOT_ANTISEMITIC = os.getenv("MONGODB_COL_NOT_ANTISEMITIC", "not_antisemitic_collection")