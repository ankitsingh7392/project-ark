# 🚀 LexiScan: Enterprise Text Classification Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![NLP](https://img.shields.io/badge/NLP-Bag_of_Words-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Overview
**LexiScan** is a lightweight, high-performance Natural Language Processing (NLP) pipeline built on the **Bag of Words (BoW)** architecture. Designed for enterprise environments, it automatically categorizes large volumes of text data—such as customer support tickets, product reviews, or legal documents—with high accuracy and minimal computational overhead.

Unlike heavy Large Language Models (LLMs), LexiScan provides transparent, explainable predictions and runs efficiently on standard hardware, making it ideal for real-time triage and classification.

## ✨ Core Features
* **Custom Tokenization & Cleaning:** Implements targeted stop-word removal to reduce noise while preserving context-critical terminology (e.g., negative sentiment words).
* **Sparse Matrix Optimization:** Handles high-dimensionality vocabulary efficiently, preventing memory bloat ("The Curse of Dimensionality").
* **TF-IDF Weighting:** (Optional) Upgrades raw word counts to Term Frequency-Inverse Document Frequency to highlight unique, document-specific keywords.
* **Explainable AI:** Easily extract which specific words triggered a classification decision.

## 🏗️ Architecture & How It Works
1. **Data Ingestion:** Reads labeled text data (e.g., CSV, JSON).
2. **Preprocessing:** Lowercases text, removes punctuation, and applies a custom stop-word filter.
3. **Vectorization:** Converts text into numerical vectors using `CountVectorizer` (Bag of Words).
4. **Model Training:** Trains a lightweight classifier (e.g., Naive Bayes or Logistic Regression) on the resulting sparse matrix.
5. **Inference:** Accepts new, unseen text and outputs a predicted category with a confidence score.

## 🛠️ Tech Stack
* **Language:** Python 3.14
* **Data Processing:** Pandas, NumPy
* **NLP & ML:** Scikit-Learn (for BoW and Classification), NLTK (for Stop Words)

## 🚀 Getting Started

### Prerequisites
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/ankitsingh7392/project-ark.git 
cd lexiscan
pip install uv
uv sync
uv run python main.py
