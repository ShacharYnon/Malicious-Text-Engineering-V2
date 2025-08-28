from features import SentimentEnhancer
from weapons_detector import WeaponsDetector
import logging
import os
from typing import List, Dict, Any
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnricherService:
    def __init__(self, weapons_list: List[str]):
        self.sentiment_enhancer = SentimentEnhancer()
        self.weapons_detector = WeaponsDetector(weapons_list)
        
    def enrich(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich documents with sentiment analysis and weapons detection

        Args:
            documents (List[Dict[str, Any]]): List of documents to enrich

        Returns:
            List[Dict[str, Any]]: List of enriched documents
        """
        try:
            docs_with_sentiment = self.sentiment_enhancer.enrich_documents(documents)
            fully_enriched_docs = self.weapons_detector.detect_weapons(docs_with_sentiment)
            return fully_enriched_docs
        except Exception as e:
            logger.error(f"Error enriching documents: {e}")
            raise RuntimeError(f"Error enriching documents: {e}")