from typing import Iterable, Dict, Any, List
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from .. import config
import logging
logger = logging.getLogger(__name__)
class MongoDAL:
    """
    Data access layer for MongoDB collections used by the persister service.
    """

    def __init__(self, uri: str, db_name: str, coll_antisemitic: str, coll_not_antisemitic: str) -> None:
        self._client = MongoClient(uri)
        self._db = self._client[db_name]
        self._antisemitic: Collection = self._db[coll_antisemitic]
        self._not_antisemitic: Collection = self._db[coll_not_antisemitic]

    def insert_antisemitic(self, docs: Iterable[Dict[str, Any]]) -> int:
        documents: List[Dict[str, Any]] = [d for d in docs if isinstance(d, dict)]
        if not documents:
            logger.warning("No valid documents to insert into antisemitic collection.")
            return 0
        result = self._antisemitic.insert_many(documents, ordered=False)
        logger.info(f"Inserted {len(result.inserted_ids)} documents into antisemitic collection.")
        return len(result.inserted_ids)

    def insert_not_antisemitic(self, docs: Iterable[Dict[str, Any]]) -> int:
        documents: List[Dict[str, Any]] = [d for d in docs if isinstance(d, dict)]
        if not documents:
            logger.warning("No valid documents to insert into not_antisemitic collection.")
            return 0
        result = self._not_antisemitic.insert_many(documents, ordered=False)
        logger.info(f"Inserted {len(result.inserted_ids)} documents into not_antisemitic collection.")
        return len(result.inserted_ids)


# if __name__ == "__main__":
#     dal = MongoDAL(
#         uri=config.MONGO_URI,
#         db_name=config.MONGO_DB,
#         coll_antisemitic=config.MONGODB_COL_ANTISEMITIC,
#         coll_not_antisemitic=config.MONGODB_COL_NOT_ANTISEMITIC,
#     )
#     test_docs = [
#         {"text": "This is a test antisemitic document.", "timestamp": 1625077765},
#         {"text": "Another antisemitic example.", "timestamp": 1625077766},
#     ]
#     inserted_count = dal.insert_antisemitic(test_docs)
#     print(f"Inserted {inserted_count} documents into antisemitic collection.")