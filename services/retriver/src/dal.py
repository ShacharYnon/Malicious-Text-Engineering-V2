from .connector import DatabaseConnection
from .. import config
from typing import List, Dict, Any
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
    
    def get_oldest_documents(self, time_stamp: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve the 100 oldest documents from the collection by timestamp
        
        Args:
            limit (int): Number of documents to retrieve
            time_stamp (str): Field name for timestamp sorting
        Returns:
            List[Dict[str, Any]]: List of documents
        """
        try:
            documents = list(self.collection.find().sort(time_stamp, 1).limit(limit))
            logger.info(f"Retrieved {len(documents)} oldest documents from the collection")
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise RuntimeError(f"Error retrieving documents: {e}")
    

if __name__ == "__main__":
    dal = DalMongo()
    docs = dal.get_oldest_documents(time_stamp="2020-03-16T13:43:43.000+00:00", limit=100)
    for doc in docs:
        print(doc)