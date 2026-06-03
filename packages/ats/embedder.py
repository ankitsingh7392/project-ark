"""TF-IDF weighted Word2Vec document embedder.

This is the core innovation: instead of plain averaging of word vectors,
we weight each word's vector by its TF-IDF score so domain-specific terms
dominate the document representation.
"""

from pathlib import Path

from gensim.models import KeyedVectors
from preprocessor import Preprocessor
from sklearn.feature_extraction.text import TfidfVectorizer


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
