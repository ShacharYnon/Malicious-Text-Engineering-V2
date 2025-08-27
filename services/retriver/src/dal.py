from .connector import DatabaseConnection
from pymongo import ASCENDING
from datetime import datetime
from .. import config
from typing import List, Dict, Any, Generator, Optional
import logging
logger = logging.getLogger(__name__)

class DalMongo:
    """"
    Data Access Layer for MongoDB retrive 100 most oldest documents
    """
    def __init__(self):
        self.db_connection = DatabaseConnection()
        self.db = self.db_connection.connect()
        self.collection = self.db[config.MONGODB_COL]
        self.time_stamp = None
        
    def get_oldest_documents(self, limit: int = 100) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Retrieve the oldest documents from the collection by timestamp
        
        Args:
            limit (int): Number of documents to retrieve default = 100
        Returns:
            Generator[List[Dict[str, Any]], None, None]:
        """
        try:
            while True:
                query = {}
                if self.time_stamp:
                    print(f"time stamp for text check:{self.time_stamp}\n")
                    query = {"CreateDate":{"$gt":self.time_stamp}}
                cursor = (
                    self.collection.find(query)
                    .sort("CreateDate",ASCENDING)
                    .limit(limit)
                )
                docs = list(cursor)
                logger.info(f"Retrieved {len(docs)} oldest documents from the collection")
                if not docs:
                    break
                yield docs
                self.time_stamp = docs[-1]["CreateDate"]
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise RuntimeError(f"Error retrieving documents: {e}")
    

# if __name__ == "__main__":
#     dal = DalMongo()
#     docs = dal.get_oldest_documents(limit=2)
#     # print(type(docs))
#     for doc_batch in docs:
#         # print(type(doc_batch))
#         for doc in doc_batch:
#             print(1)
        
        