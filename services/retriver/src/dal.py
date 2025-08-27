from connector import DatabaseConnection
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
    
    def get_oldest_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve the oldest documents from the collection
        
        Args:
            limit (int): Number of documents to retrieve
        
        Returns:
            List[Dict[str, Any]]: List of documents
        """
        try:
            documents = list(self.collection.find().sort('timestamp', 1).limit(limit))
            logger.info(f"Retrieved {len(documents)} oldest documents from the collection")
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise RuntimeError(f"Error retrieving documents: {e}")