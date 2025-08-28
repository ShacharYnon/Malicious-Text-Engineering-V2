from venv import logger
import nltk
import logging
from typing import List, Dict, Any
import pandas as pd

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
logger = logging.getLogger(__name__)


class Enricher:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

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
                text = doc.get("text", "")
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
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"


if __name__ == "__main__":
    sample_docs = [
        {"_id": 1, "text": "I love programming!"},
        {"_id": 2, "text": "I hate bugs."},
    ]
    enricher = Enricher()
    enriched = enricher.enrich_documents(sample_docs)
    for doc in enriched:
        print(doc)