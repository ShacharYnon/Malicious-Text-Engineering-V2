import re
import nltk
from typing import List
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


_WORD_RE = re.compile(r"\w+")
_NON_ALNUM_SPACE_RE = re.compile(r"[^a-zA-Z0-9\s]")


def _ensure_nltk_data() -> None:
    """
    Ensure required NLTK corpora are available.
    Downloads 'stopwords', 'wordnet', and 'omw-1.4' if missing.
    """
    for pkg in ["stopwords", "wordnet", "omw-1.4"]:
        try:
            nltk.data.find(f"corpora/{pkg}")
        except LookupError:
            nltk.download(pkg, quiet=True)


class DataProcessor:
    """
    A class for preprocessing text data: lowercasing, special-char removal,
    stopword removal, and lemmatization.
    """

    def __init__(self, language: str = "english") -> None:
        """
        Initialize the processor with a stopword set and a lemmatizer.

        Args:
            language: Language name for NLTK stopwords (default: "english").
        """
        _ensure_nltk_data()
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from the input text.

        Args:
            text: The input text.

        Returns:
            The text with stopwords removed.
        """
        tokens = _WORD_RE.findall(text)
        filtered_tokens = [w for w in tokens if w not in self.stop_words]
        return " ".join(filtered_tokens)

    def remove_special_characters(self, text: str) -> str:
        """
        Remove special characters from the input text, preserving letters,
        digits, and spaces.

        Args:
            text: The input text.

        Returns:
            The text with special characters removed.
        """
        return _NON_ALNUM_SPACE_RE.sub("", text)

    def to_lowercase(self, text: str) -> str:
        """
        Convert the input text to lowercase.

        Args:
            text: The input text.

        Returns:
            The lowercased text.
        """
        return text.lower()

    def lemmatize(self, text: str) -> str:
        """
        Lemmatize tokens in the input text using WordNet.

        Args:
            text: The input text.

        Returns:
            The lemmatized text.
        """
        tokens = _WORD_RE.findall(text)
        lemmas = [self.lemmatizer.lemmatize(w) for w in tokens]
        return " ".join(lemmas)

    def preprocess(self, text: str) -> str:
        """
        Apply standard preprocessing: lowercase → strip specials → remove
        stopwords → lemmatize.

        Args:
            text: The input text.

        Returns:
            The preprocessed text.
        """
        text = self.to_lowercase(text)
        text = self.remove_special_characters(text)
        text = self.remove_stopwords(text)
        text = self.lemmatize(text)
        return text


if __name__ == "__main__":
    processor = DataProcessor()
    sample_text = "This is a sample text! It includes numbers 123 and special characters #@$. and Gun AK-47"
    preprocessed_text = processor.preprocess(sample_text)
    print(f"Original Text: {sample_text}")
    print(f"Preprocessed Text: {preprocessed_text}")