from .. import config
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import os
from collections import Counter
from typing import Dict, Optional
import uuid
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

class Features:
    """
    a processing class for tweets data
    """
    
    def __init__(self, dataframe, column="Text"):
        """Initialize TweetsProcessor with dataframe and configuration"""
        logger.info("Initializing TweetsProcessor...")
        
        try:
            self.df = dataframe
            self.message_column = column
            logger.info(f"DataFrame shape: {dataframe.shape}, using column: {column}")
            
            # Load weapons list
            logger.info("Loading weapons list...")
            self.weapons_set = self._load_weapons_list()
            logger.info(f"Loaded {len(self.weapons_set)} weapons from weapons.txt")
            
            # Initialize sentiment analyzer
            logger.info("Initializing sentiment analyzer...")
            self.sia = self._initialize_sentiment_analyzer()
            
            logger.info("TweetsProcessor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TweetsProcessor: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error("Full traceback:", exc_info=True)
            raise

    def load_weapons_list(self):
        """Load weapons list from file once during initialization with detailed logging"""
        weapons_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'weapon_list.txt')
        logger.info(f"Looking for weapons file at: {weapons_file_path}")
        
        try:
            if not os.path.exists(weapons_file_path):
                logger.error(f"Weapons file does not exist at path: {weapons_file_path}")
                return set()
            
            with open(weapons_file_path, 'r') as file:
                weapons_list = {line.strip().lower() for line in file if line.strip()}
                logger.info(f"Successfully loaded {len(weapons_list)} weapons from file")
                return weapons_list
                
        except FileNotFoundError:
            logger.error(f"Weapons file not found at {weapons_file_path}")
            return set()
        except PermissionError:
            logger.error(f"Permission denied when trying to read weapons file at {weapons_file_path}")
            return set()
        except Exception as e:
            logger.error(f"Unexpected error loading weapons file: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return set()

    def initialize_sentiment_analyzer(self):
        """Initialize sentiment analyzer once during initialization with detailed logging"""
        logger.info("Downloading VADER lexicon for sentiment analysis...")
        
        try:
            nltk.download('vader_lexicon', quiet=True)
            logger.info("VADER lexicon downloaded successfully")
            
            analyzer = SentimentIntensityAnalyzer()
            logger.info("SentimentIntensityAnalyzer initialized successfully")
            return analyzer
            
        except Exception as e:
            logger.error(f"Could not initialize sentiment analyzer: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.info("Sentiment analysis will not be available")
            return None

    def get_sentiment_for_text(self, text: str) -> str:
        """
        Analyze the sentiment of a single text with detailed logging.
        
        Args:
            text: The text to analyze
            
        Returns:
            Sentiment label (positive/negative/neutral)
        """
        logger.info("Starting sentiment analysis...")
        
        if not self.sia:
            logger.info("Sentiment analyzer not available, returning 'unknown'")
            return "unknown"
        
        if not text:
            logger.info("Empty text provided for sentiment analysis")
            return "unknown"
        
        try:
            scores = self.sia.polarity_scores(text)
            compound_score = scores['compound']
            sentiment = self._classify_sentiment(compound_score)
            
            logger.info(f"Sentiment scores: {scores}, classified as: {sentiment}")
            return sentiment
            
        except Exception as e:
            logger.error(f"Error during sentiment analysis: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return "error"
    
    def classify_sentiment(self, compound_score)-> str:
        """
        Classify sentiment based on compound score.

        Returns: a sens tag by score.
        """
        if compound_score >= 0.5:
            return "positive"
        elif compound_score <= -0.5:
            return "negative text"
        else:
            return "neutral text"
        
    def extract_weapons_from_text(self, text: str) -> list:
        """
        Extract weapon names (single or multi-word) from text with detailed logging.
        
        Args:
            text: Text to search for weapons
            
        Returns:
            List of weapons found in text
        """
        logger.info("Starting weapons extraction...")
        
        if not text:
            logger.info("Empty text provided for weapons extraction")
            return []
        
        if not self.weapons_set:
            logger.info("No weapons list loaded, cannot extract weapons")
            return []
        
        try:
            text_lower = text.lower()
            found_weapons = {weapon.lower() for weapon in self.weapons_set if weapon in text_lower}
            weapons_list = list(found_weapons)
            
            if weapons_list:
                logger.info(f"Found {len(weapons_list)} weapons: {weapons_list}")
            else:
                logger.info("No weapons found in text")
            
            return weapons_list
            
        except Exception as e:
            logger.error(f"Error extracting weapons from text: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return []

    def process_single_tweet(self, text: str, tweet_id: Optional[str] = None) -> Dict:
        """
        Process a single tweet text and return analysis results with detailed logging.
        
        Args:
            text: Tweet text to analyze
            tweet_id: Optional tweet ID
            
        Returns:
            Dictionary containing analysis results
        """
        logger.info(f"Processing single tweet with ID: {tweet_id}")
        
        try:
            if not text:
                text = ""
                logger.info(f"Empty text provided for tweet ID: {tweet_id}")

            # Get sentiment
            logger.info("Analyzing sentiment...")
            try:
                sentiment = self._get_sentiment_for_text(text)
                logger.info(f"Sentiment analysis result: {sentiment}")
            except Exception as e:
                logger.error(f"Error analyzing sentiment for tweet {tweet_id}: {str(e)}")
                sentiment = "neutral"
            
            # Extract weapons
            logger.info("Extracting weapons...")
            try:
                weapons_list = self._extract_weapons_from_text(text)
                weapons_str = ", ".join(weapons_list) if weapons_list else "none"
                logger.info(f"Weapons detected: {weapons_str}")
            except Exception as e:
                logger.error(f"Error extracting weapons for tweet {tweet_id}: {str(e)}")
                weapons_str = "none"
            
            result = {
                "sentiment": sentiment,
                "original_text": text,     ##==========================================================================
                "weapons_detected": weapons_str
            }
            
            logger.info(f"Successfully processed tweet {tweet_id}")
            return result
            
        except Exception as e:
            logger.error(f"Critical error processing tweet {tweet_id}: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error("Full traceback:", exc_info=True)
            
            # Return error result instead of failing completely
            return {
                "sentiment": "error",
                "original_text": text,
                "weapons_detected": "error",
                "error": str(e)
            }