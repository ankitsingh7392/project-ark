"""LexiScan: CPU-only text classifier for routing tickets, emails and documents.

Text is vectorised with TF-IDF (or raw Bag-of-Words counts) and classified by a
Multinomial Naïve Bayes model. Predictions carry a confidence percentage, and
anything below a configurable threshold is returned as ``"Unknown"`` so that
low-confidence inputs can be escalated rather than mis-routed.
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

UNKNOWN_LABEL = "Unknown"


class LexiModel:
    """Vectoriser + Naïve Bayes classifier with confidence-thresholded routing."""

    def __init__(self, use_tfidf: bool = True):
        self.use_tfidf = use_tfidf
        if use_tfidf:
            self.vectorizer = TfidfVectorizer(
                stop_words="english", ngram_range=(1, 2), min_df=1, max_features=5000
            )
        else:
            self.vectorizer = CountVectorizer(stop_words="english")
        self.classifier = MultinomialNB()

    def train(self, data_path: str, text_column: str, label_column: str) -> None:
        """Fit the vectoriser and classifier on a labelled CSV."""
        df = pd.read_csv(data_path)
        texts = df[text_column].astype(str).str.lower()
        features = self.vectorizer.fit_transform(texts)
        self.classifier.fit(features, df[label_column])

    def predict(self, text: str, threshold: float = 50) -> dict:
        """Classify ``text``; return ``{"category", "confidence"}``.

        ``confidence`` is the top class probability in percent. If it falls
        below ``threshold`` the category is ``"Unknown"``.
        """
        features = self.vectorizer.transform([text.lower()])
        prediction = str(self.classifier.predict(features)[0])
        confidence = float(self.classifier.predict_proba(features)[0].max()) * 100
        if confidence < threshold:
            prediction = UNKNOWN_LABEL
        return {"category": prediction, "confidence": round(confidence, 2)}
