"""Text cleaning and preprocessing utilities."""

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data on first import
for resource in ["punkt", "stopwords", "wordnet", "averaged_perceptron_tagger"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)


class Preprocessor:
    """Cleans and tokenizes text for embedding."""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words("english"))
        # Keep some technically meaningful short tokens
        self.allow_short = {"ai", "ml", "ui", "ux", "qa", "ci", "cd", "go", "r"}

    def clean(self, text: str) -> str:
        """Lowercase, strip URLs, emails, and excess whitespace."""
        text = text.lower()
        text = re.sub(r"http\S+|www\.\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)
        text = re.sub(r"[^\w\s+#./-]", " ", text)  # keep + # . / - for tech terms
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> list[str]:
        """Tokenize, remove stopwords, lemmatize."""
        cleaned = self.clean(text)
        tokens = word_tokenize(cleaned)
        result = []
        for tok in tokens:
            if tok in self.allow_short:
                result.append(tok)
                continue
            if len(tok) < 2 or tok in self.stopwords or tok in string.punctuation:
                continue
            result.append(self.lemmatizer.lemmatize(tok))
        return result
