from pymongo import MongoClient
from pymongo.database import Database
from .. import config
import logging
logger = logging.getLogger(__name__)
class DatabaseConnection:
    """
    MongoDB connection manager
    """
    
    def __init__(self):
        """
        Initialize database connection
        """
        self.client = None
        self.database = None
    
    def connect(self) -> Database:
        """
        Establish connection to MongoDB
        
        Returns:
            Database: MongoDB database instance
        """
        try:
            self.client = MongoClient(config.MONGODB_URI)
            self.database = self.client[config.MONGODB_DATABASE]
            # Test the connection
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB at {config.MONGODB_URI}, using database '{config.MONGODB_DATABASE}'")
            return self.database
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
    
    def disconnect(self):
        """
        Close database connection
        """
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")