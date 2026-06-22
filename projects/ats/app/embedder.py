"""TF-IDF weighted Word2Vec document embedder.

This is the core innovation: instead of plain averaging of word vectors,
we weight each word's vector by its TF-IDF score so domain-specific terms
dominate the document representation.
"""

from pathlib import Path

import numpy as np
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer

from app.preprocessor import Preprocessor


class TfIdfWord2VecEmbedder:
    """Build document vectors as TF-IDF weighted averages of Word2Vec embeddings."""

    def __init__(self, model_path: str | None = None, vector_size: int = 300):
        self.preprocessor = Preprocessor()
        self.vector_size = vector_size
        self.tfidf: TfidfVectorizer | None = None
        self.word_vectors: KeyedVectors | None = None
        if model_path and Path(model_path).exists():
            self.load_word_vectors(model_path)

    def load_word_vectors(self, path: str) -> None:
        """Load pre-trained Word2Vec (KeyedVectors format)."""
        self.word_vectors = (
            KeyedVectors.load(path)
            if path.endswith(".kv")
            else KeyedVectors.load_word2vec_format(path, binary=path.endswith(".bin"))
        )

    def fit_tfidf(self, corpus: list[str]) -> None:
        """Fit the TF-IDF vectorizer on a corpus (use both resumes and JDs)."""
        tokenized = [" ".join(self.preprocessor.tokenize(t)) for t in corpus]
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 1),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True,
        )
        self.tfidf.fit(tokenized)

    def embed(self, text: str) -> np.ndarray:
        """Convert a document to a single vector."""
        if self.tfidf is None or self.word_vectors is None:
            raise RuntimeError(
                "Embedder not initialized. Call load_word_vectors() and fit_tfidf() first."
            )

        tokens = self.preprocessor.tokenize(text)
        if not tokens:
            return np.zeros(self.vector_size)

        tfidf_scores = self._token_tfidf_scores(tokens)

        vectors, weights = [], []
        for tok in tokens:
            if tok in self.word_vectors and tok in tfidf_scores:
                vectors.append(self.word_vectors[tok])
                weights.append(tfidf_scores[tok])

        if not vectors:
            return np.zeros(self.vector_size)

        vectors = np.asarray(vectors)
        weights = np.asarray(weights).reshape(-1, 1)
        doc_vec = (vectors * weights).sum(axis=0) / (weights.sum() + 1e-9)
        return doc_vec

    def _token_tfidf_scores(self, tokens: list[str]) -> dict:
        """Map each token to its TF-IDF weight."""
        joined = " ".join(tokens)
        vec = self.tfidf.transform([joined]).toarray()[0]
        feature_names = self.tfidf.get_feature_names_out()
        return {feature_names[i]: vec[i] for i in vec.nonzero()[0]}
