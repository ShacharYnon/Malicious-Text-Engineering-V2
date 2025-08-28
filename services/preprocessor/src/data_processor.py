import re
from typing import List
import cleantext
from stopwordsiso import stopwords
from nltk.stem import PorterStemmer
import logging

logger = logging.getLogger(__name__)


class TextCleaner:
    """
    Stateless-ish cleaner: normalize, remove stopwords, and apply stemming.
    Uses libraries that don't require runtime downloads (good for OpenShift).
    """

    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.stopwords = stopwords(lang)
        self.stemmer = PorterStemmer()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def clean_central(self, text: str) -> str:
        """
        Central cleaning pipeline:
        1) normalize (lower, strip currency, remove punct)
        2) tokenize without punkt
        3) stopword removal
        4) stemming
        """
        cleaned = cleantext.clean(
            text,
            lower=True,
            no_currency_symbols=True,
            no_punct=True,
            strip_lines=True,
        )
        tokens = self._tokenize(cleaned)

        try:
            filtered = [t for t in tokens if t not in self.stopwords]
            stemmed = [self.stemmer.stem(t) for t in filtered]
            logger.debug("Text cleaned successfully")
        except Exception as e:
            logger.error(f"Error during text cleaning: {e}")
            raise RuntimeError(f"Error during text cleaning: {e}")

        return " ".join(stemmed)
