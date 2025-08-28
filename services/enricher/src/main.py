from .features import SentimentEnhancer
from .weapons_detector import WeaponsDetector
import logging
import os
from typing import List, Dict, Any
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnricherService:
    def __init__(self):
        self.sentiment_enhancer = SentimentEnhancer()
        weapons_list = self._load_weapons()
        self.weapons_detector = WeaponsDetector(weapons_list)

    def _load_weapons(self)->List[str]:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        weapons_file_path = os.path.join(BASE_DIR, "..", "..", "..", "data", "weapon_list.txt")
        weaponslist = []
        try:
            with open(weapons_file_path, 'r') as file:
                weaponslist = [line.strip() for line in file if line.strip()]
            logger.info(f"Loaded {len(weaponslist)} weapons from {weapons_file_path}")
            return weaponslist
        except Exception as e:
            logger.error(f"Error loading weapons list: {e}")
            raise RuntimeError(f"Error loading weapons list: {e}")


        
    def enrich(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich documents with sentiment analysis and weapons detection

        Args:
            documents (List[Dict[str, Any]]): List of documents to enrich

        Returns:
            List[Dict[str, Any]]: List of enriched documents
        """
        try:
            # First apply sentiment analysis
            sentiment_enriched_docs = self.sentiment_enhancer.enrich_documents(documents)
            # Then apply weapons detection
            fully_enriched_docs = self.weapons_detector.detect_weapons(sentiment_enriched_docs)
            return fully_enriched_docs
        except Exception as e:
            logger.error(f"Error enriching documents: {e}")
            raise RuntimeError(f"Error enriching documents: {e}")
        
    
if __name__ == "__main__":
    sample_docs = [
        {"_id": 1, "Cleaned_Text": "This is a test text with a gun."},
        {"_id": 2, "Cleaned_Text": "No weapons here."},
        {"_id": 3, "Cleaned_Text": "Another text with a knife and a rifle."}
    ]
    enricher = EnricherService()
    enriched_docs = enricher.enrich(sample_docs)
    for doc in enriched_docs:
        print(doc)