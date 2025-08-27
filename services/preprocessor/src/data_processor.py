import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

text = "This is a sample sentence showing stopword removal."

tokens = re.findall(r"\w+", text.lower())

stop_words = set(stopwords.words("english"))

filtered_tokens = [word for word in tokens if word not in stop_words]

print("Original:", tokens)
print("Filtered:", filtered_tokens)
