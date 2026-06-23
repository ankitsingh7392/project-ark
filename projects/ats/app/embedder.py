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
        # Weight applied to in-vocabulary terms that the document itself does not
        # surface via TF-IDF; set when ``fit_tfidf`` runs.
        self._fallback_weight: float = 1.0
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
        """Fit the TF-IDF vectorizer on a corpus (use both resumes and JDs).

        ``min_df`` scales with corpus size: a fixed ``min_df=2`` collapses the
        vocabulary to almost nothing on small bootstrap corpora (every term that
        appears in only one document is discarded), which silently disables the
        weighting. We require a term in ≥2 documents only once there are enough
        documents for that to be meaningful.
        """
        tokenized = [" ".join(self.preprocessor.tokenize(t)) for t in corpus]
        min_df = 2 if len(tokenized) >= 10 else 1
        self.tfidf = TfidfVectorizer(
            ngram_range=(1, 1),
            min_df=min_df,
            max_df=1.0,
            sublinear_tf=True,
        )
        self.tfidf.fit(tokenized)
        # Out-of-vocabulary terms fall back to the mean IDF so domain words the
        # corpus has not seen still contribute their Word2Vec semantics.
        self._fallback_weight = float(np.mean(self.tfidf.idf_)) if self.tfidf.idf_.size else 1.0

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
            if tok not in self.word_vectors:
                continue
            # Use the document's TF-IDF weight when the term is in the fitted
            # vocabulary; otherwise fall back so out-of-vocabulary domain terms
            # still contribute their Word2Vec semantics instead of being dropped.
            vectors.append(self.word_vectors[tok])
            weights.append(tfidf_scores.get(tok, self._fallback_weight))

        if not vectors:
            return np.zeros(self.vector_size)

        vectors = np.asarray(vectors)
        weights = np.asarray(weights).reshape(-1, 1)
        doc_vec = (vectors * weights).sum(axis=0) / (weights.sum() + 1e-9)
        return doc_vec

    def token_weights(self, text: str) -> dict:
        """Return a ``{token: weight}`` map for a document.

        Weights are the document's TF-IDF scores where available, falling back to
        the mean IDF for in-corpus-unseen terms. Used to surface how important
        each term in a job description is (e.g. for skill-gap importance).
        """
        if self.tfidf is None:
            return {}
        tokens = self.preprocessor.tokenize(text)
        scores = self._token_tfidf_scores(tokens)
        return {tok: scores.get(tok, self._fallback_weight) for tok in tokens}

    def _token_tfidf_scores(self, tokens: list[str]) -> dict:
        """Map each token to its TF-IDF weight."""
        joined = " ".join(tokens)
        vec = self.tfidf.transform([joined]).toarray()[0]
        feature_names = self.tfidf.get_feature_names_out()
        return {feature_names[i]: vec[i] for i in vec.nonzero()[0]}
