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
    
    def get_oldest_documents(self, limit: int = 100) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Retrieve the oldest documents from the collection by timestamp
        
        Args:
            limit (int): Number of documents to retrieve default = 100
        Returns:
            Generator[List[Dict[str, Any]], None, None]:
        """
        try:
            last_timestamp: Optional[datetime] = None
            while True:
                query = {}
                if last_timestamp:
                    query = {"CreateDate":{"$gt":last_timestamp}}
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
                last_timestamp = docs[-1]["CreateDate"]
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise RuntimeError(f"Error retrieving documents: {e}")
    


   




if __name__ == "__main__":
    dal = DalMongo()
    docs = dal.get_oldest_documents(limit=2)
    for doc_batch in docs:
        for doc in doc_batch:
            print(doc)