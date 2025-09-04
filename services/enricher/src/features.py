import os
import logging
from typing import List, Dict, Any

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")
os.environ['NLTK_DATA'] = '/usr/local/share/nltk_data'


logger = logging.getLogger(__name__)


class SentimentEnhancer:
    def __init__(self):
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except LookupError as e:
            logger.error(f"NLTK data not found: {e}")
            logger.error("Make sure vader_lexicon is installed in the Docker image")
            raise

    def enrich_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich documents with sentiment analysis and word count

        Args:
            documents (List[Dict[str, Any]]): List of documents to enrich

        Returns:
            List[Dict[str, Any]]: List of enriched documents
        """
        enriched_docs = []
        for doc in documents:
            try:
                text = doc.get("Cleaned_Text", "")
                sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
                sentiment_scores = self._point_sentiment(sentiment_scores['compound'])
                enriched_doc = {
                    **doc,
                    "Sentiment": sentiment_scores,
                }
                enriched_docs.append(enriched_doc)
            except Exception as e:
                logger.error(f"Error enriching document {doc.get('_id')}: {e}")
                continue
        return enriched_docs

    def _point_sentiment(self, score: float) -> str:
        """"
        Convert compound sentiment score to categorical sentiment
        Args:
            score (float): Compound sentiment score
            Returns:
            str: Categorical sentiment ("positive", "negative", "neutral")
            """
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"


# if __name__ == "__main__":
#     sample_docs = [
#         {"_id": 1, "Cleaned_Text": "I love programming!"},
#         {"_id": 2, "Cleaned_Text": "I hate bugs."},
#     ]
#     enricher = SentimentEnhancer()
#     enriched = enricher.enrich_documents(sample_docs)
#     for doc in enriched:
#         print(doc)