import re
from typing import List
import cleantext
from stopwordsiso import stopwords
from nltk.stem import PorterStemmer
import logging
logger = logging.getLogger(__name__)
class TextCleaner:
    def __init__(self, lang: str = "en"):
        self.lang = lang
        self.stopwords = stopwords(lang) 
        self.stemmer = PorterStemmer()

    def _tokenize(self, text: str) -> List[str]:
        logger.info("Tokenizing text")
        return re.findall(r"[a-zA-Z0-9']+", text)

    def clean_central(self, text: str) -> str:
        cleaned = cleantext.clean(
            text,
            lower=True,
            no_currency_symbols=True,
            no_punct=True,
            no_line_breaks=True,
        )
        tokens = self._tokenize(cleaned)
        try:
            filtered = [t for t in tokens if t not in self.stopwords]
            stemmed = [self.stemmer.stem(t) for t in filtered]
            logger.info("Text cleaned successfully")
        except Exception as e:
            logger.error(f"Error during text cleaning: {e}")
            raise RuntimeError(f"Error during text cleaning: {e}")
        return " ".join(stemmed)

if __name__ == "__main__":
    cleaner = TextCleaner()
    sample_text = "This is a Sample pilow! With Punctuation, and stopwords. AK-47   Guns"
    print(cleaner.clean_central(sample_text))
