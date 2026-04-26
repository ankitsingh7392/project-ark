from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB 
import pandas as pd

class LexiModel:
    
    def __init__(self, use_tfidf=False):
        # 1. Setting up your Bag of Words!
        self.use_tfidf = use_tfidf
        if use_tfidf:
            self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), min_df=1, max_features=5000)
        else:
            self.vectorizer = CountVectorizer(stop_words="english")
        
        # 2. Set up the Classifier (The Brain)
        self.classifier = MultinomialNB()
    
    def train(self, data_path, text_column, label_column):
        print(f"Training the model now... {data_path}")
        df = pd.read_csv(data_path)
        # Converting text to Bag of Words vectors...
        df[text_column] = df[text_column].str.lower()
        X_vectors = self.vectorizer.fit_transform(df[text_column])
        y_labels = df[label_column]
        print("Training the classifier...\n")
        self.classifier.fit(X_vectors, y_labels)
        
        
    
    def predict(self, text, threshold=50):
        # Convert the new sentence into a vector using the same vocabulary
        text_vector = self.vectorizer.transform([text])
        # Make the mathematical prediction
        prediction = self.classifier.predict(text_vector)[0]
        # Calculate how confident the computer is (0 to 100%)
        probabilities = self.classifier.predict_proba(text_vector)[0]
        confidence = max(probabilities) * 100
        if confidence < threshold:
            prediction = "Unknown"
        
        return {
            "category": prediction,
            "confidence": round(confidence, 2)
        }
        