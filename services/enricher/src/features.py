from typing import Optional, Dict, Iterable
import math
import pandas as pd

try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    _VADER_AVAILABLE = True
except Exception:
    _VADER_AVAILABLE = False


class SentimentBatchProcessor:
    """
    Batch sentiment processor for a pandas DataFrame.
    - Input: DataFrame and a text column name (default: 'Text').
    - Output: Same DataFrame with an added 'sentiment' column (and 'compound_score' if keep_scores=True).
    - Classification thresholds:
        compound >=  0.5 -> 'positive'
        compound <= -0.5 -> 'negative text'
        else              -> 'neutral text'

    If NLTK VADER is available, uses it. Otherwise, falls back to a small built-in lexicon scorer.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        text_column: str = "Text",
        keep_scores: bool = False,
        custom_lexicon: Optional[Dict[str, int]] = None,
    ) -> None:
        """
        Initialize the processor.

        Args:
            dataframe: Pandas DataFrame containing a text column.
            text_column: Name of the column with text to analyze.
            keep_scores: If True, also adds 'compound_score' column.
            custom_lexicon: Optional fallback lexicon {word: polarity}. Used only if VADER is unavailable.
        """
        if text_column not in dataframe.columns:
            raise KeyError(f"Column '{text_column}' not found in DataFrame")
        self.df = dataframe
        self.text_column = text_column
        self.keep_scores = keep_scores

        self._sia = None
        if _VADER_AVAILABLE:
            try:
                nltk.download("vader_lexicon", quiet=True)
                self._sia = SentimentIntensityAnalyzer()
            except Exception:
                self._sia = None

        self._lexicon = custom_lexicon or {
            "good": 2, "great": 3, "excellent": 4, "amazing": 4, "happy": 3, "love": 3,
            "like": 2, "awesome": 4, "fantastic": 4, "win": 2, "positive": 2, "success": 2,
            "bad": -2, "terrible": -3, "awful": -4, "sad": -2, "hate": -3, "angry": -2,
            "worse": -2, "worst": -4, "fail": -3, "loss": -2, "negative": -2, "disaster": -4,
        }

    def process(self) -> pd.DataFrame:
        """
        Process all rows and return a new DataFrame with 'sentiment' (and optionally 'compound_score').

        Returns:
            DataFrame with added sentiment classification per row.
        """
        scores = self.df[self.text_column].apply(self._score_text_safe)
        sentiments = scores.apply(self._classify_sentiment)
        out = self.df.copy()
        out["sentiment"] = sentiments
        if self.keep_scores:
            out["compound_score"] = scores
        return out

    def _score_text_safe(self, x) -> float:
        """
        Safe scorer: accepts any input, returns a compound score in [-1, 1].
        """
        text = "" if x is None else str(x)
        if not text.strip():
            return 0.0
        if self._sia is not None:
            try:
                return float(self._sia.polarity_scores(text)["compound"])
            except Exception:
                pass
        return self._fallback_compound(text)

    def _fallback_compound(self, text: str) -> float:
        """
        Lightweight lexicon-based scorer producing a compound value in [-1, 1].
        """
        tokens = self._simple_tokenize(text)
        if not tokens:
            return 0.0
        raw = sum(self._lexicon.get(tok, 0) for tok in tokens)
        denom = math.sqrt(len(tokens))
        score = raw / (4.0 * denom) 
        return max(-1.0, min(1.0, score))

    @staticmethod
    def _simple_tokenize(text: str) -> Iterable[str]:
        """
        Very simple tokenizer: lowercase alphanumerics.
        """
        return [t for t in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if t]

    @staticmethod
    def _classify_sentiment(compound_score: float) -> str:
        """
        Map compound score to the requested labels.
        """
        if compound_score >= 0.5:
            return "positive"
        if compound_score <= -0.5:
            return "negative text"
        return "neutral text"


if __name__ == "__main__":
    # Demo
    df = pd.DataFrame({
        "Text": [
            "I love this! Absolutely fantastic.",
            "This is bad. The worst experience.",
            "It's okay, nothing special.",
            None,
        ]
    })
    proc = SentimentBatchProcessor(df, text_column="Text", keep_scores=True)
    print(proc.process())
