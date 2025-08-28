import logging
from typing import List, Dict, Any



class WeaponsDetector:
    """"
    Detect weapons in text documents and enrich them with a 'Weapons_Detected' field."""
    def __init__(self, weapons_list: List[str]):
        self.weapons_list = weapons_list
        self.logger = logging.getLogger(__name__)

    def detect_weapons(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect weapons in the documents and enrich them with a 'Weapons_Detected' field.

        Args:
            documents (List[Dict[str, Any]]): List of documents to process.

        Returns:
            List[Dict[str, Any]]: List of enriched documents.
        """
        enriched_docs = []
        for doc in documents:
            try:
                text = doc.get("Cleaned_Text", "")
                detected_weapons = [weapon for weapon in self.weapons_list if weapon in text]
                enriched_doc = {
                    **doc,
                    "Weapons_Detected": detected_weapons
                }
                enriched_docs.append(enriched_doc)
            except Exception as e:
                self.logger.error(f"Error processing document {doc.get('_id')}: {e}")
                continue
        return enriched_docs
    
# if __name__ == "__main__":
#     sample_docs = [
#         {"_id": 1, "Cleaned_Text": "This is a test text with a gun."},
#         {"_id": 2, "Cleaned_Text": "No weapons here."},
#         {"_id": 3, "Cleaned_Text": "Another text with a knife and a rifle."}
#     ]
#     weapons = ["gun", "knife", "rifle"]
#     detector = WeaponsDetector(weapons)
#     enriched = detector.detect_weapons(sample_docs)
#     for doc in enriched:
#         print(doc)