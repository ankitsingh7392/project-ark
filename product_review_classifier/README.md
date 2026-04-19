<div align="center">

# 🧠 Text Feature Engineering Pipeline
### *From Raw Reviews → Intelligent Numerical Features*

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Text%20Mining-4CAF50?style=for-the-badge&logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

<br/>

> **A production-ready NLP pipeline** that scrapes real-world product reviews, preprocesses them, engineers numerical features using OHE, Bag of Words & TF-IDF, and benchmarks sentiment classifiers — all in one clean, modular codebase.

<br/>

[📖 Overview](#-overview) · [🗂️ Project Structure](#️-project-structure) · [⚙️ Pipeline](#️-pipeline) · [📊 Results](#-results--insights) · [🚀 Quickstart](#-quickstart) · [📚 Concepts](#-core-nlp-concepts)

---

</div>

<br/>

## 📖 Overview

This project builds an **end-to-end Text Processing Pipeline** on real user-generated product reviews scraped from e-commerce platforms. The pipeline transforms raw, messy text into structured numerical features ready for machine learning — covering the full journey from web scraping to model evaluation.

### ✨ What Makes This Project Stand Out

| Aspect | Detail |
|--------|--------|
| 🌐 **Real Data** | 100+ live product reviews scraped with BeautifulSoup/Selenium |
| 🔬 **3 Encoding Strategies** | One-Hot Encoding, Bag of Words, TF-IDF — compared side by side |
| 🤖 **ML Benchmarking** | Logistic Regression vs. Naïve Bayes on BoW vs. TF-IDF features |
| 📐 **Sparse Matrix Analysis** | Sparsity metrics, shape analysis, and real-world implications |
| 📝 **Full Report** | Observations, limitations, and industry use-case breakdown |

<br/>

---

## 🗂️ Project Structure

```
📦 text-feature-engineering/
│
├── 📓 notebook/
│   └── text_feature_engineering.ipynb   # Main Jupyter notebook (all tasks)
│
├── 📁 data/
│   └── reviews.csv                      # Scraped dataset (100+ reviews)
│
├── 📁 outputs/
│   ├── screenshots/                     # Output screenshots per task
│   ├── vocabulary.txt                   # Generated vocabulary list
│   └── matrices/                        # Saved sparse matrix snapshots
│
├── 📄 report.pdf                        # 1–2 page observations & conclusions
└── 📄 README.md                         # You are here
```

<br/>

---

## ⚙️ Pipeline

The project is structured into **7 sequential tasks**, forming a complete NLP feature engineering pipeline:

<br/>

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  🌐 WEB SCRAPING                                                    │
│  Flipkart / Amazon  →  100+ Reviews  →  reviews.csv                │
│                              │                                      │
│                              ▼                                      │
│  🧹 TASK 1 — PREPROCESSING                                         │
│  Lowercase → Tokenize → Remove Punctuation → Stopwords → Lemmatize │
│                              │                                      │
│                              ▼                                      │
│  📚 TASK 2 — VOCABULARY CREATION                                   │
│  Build vocab  →  Top-N frequent words  →  Vocabulary size          │
│                              │                                      │
│                              ▼                                      │
│  🔢 TASK 3 — FEATURE ENGINEERING                                   │
│  ┌──────────────┬──────────────────┬───────────────────────────┐   │
│  │  One-Hot     │  Bag of Words    │  TF-IDF                   │   │
│  │  Encoding    │  CountVectorizer │  TfidfVectorizer          │   │
│  └──────────────┴──────────────────┴───────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  📊 TASK 4 — COMPARISON ANALYSIS                                   │
│  OHE vs BoW vs TF-IDF  →  Top words per method                    │
│                              │                                      │
│                              ▼                                      │
│  🕳️  TASK 5 — SPARSE MATRIX ANALYSIS                              │
│  Shape  →  Sparsity %  →  Memory implications                      │
│                              │                                      │
│                              ▼                                      │
│  💡 TASK 6 — REAL-WORLD QUESTIONS                                  │
│  Semantic gaps  →  Industry use cases  →  TF-IDF limits            │
│                              │                                      │
│                              ▼                                      │
│  🤖 TASK 7 — SENTIMENT CLASSIFICATION                              │
│  Logistic Regression + Naïve Bayes  →  BoW vs TF-IDF benchmark    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

<br/>

---

## 📊 Results & Insights

### Feature Encoding Comparison

| Feature | One-Hot Encoding | Bag of Words | TF-IDF |
|--------|:----------------:|:------------:|:------:|
| Captures word frequency | ❌ | ✅ | ✅ |
| Penalizes common words | ❌ | ❌ | ✅ |
| Preserves word order | ❌ | ❌ | ❌ |
| Useful for small vocab | ✅ | ✅ | ✅ |
| Best for large corpora | ❌ | ⚠️ | ✅ |
| Highlights rare, key terms | ❌ | ❌ | ✅ |

<br/>

### Sentiment Classification Benchmark

| Classifier | Features | Accuracy | Precision | Recall | F1 Score |
|-----------|----------|----------|-----------|--------|----------|
| Logistic Regression | BoW | — | — | — | — |
| Logistic Regression | TF-IDF | — | — | — | — |
| Naïve Bayes | BoW | — | — | — | — |
| Naïve Bayes | TF-IDF | — | — | — | — |

> 📌 *Results populated after running the notebook on your scraped dataset.*

<br/>

### Sparse Matrix Stats

```
OHE Matrix Shape   :  (N_docs × vocab_size)
BoW Matrix Shape   :  (N_docs × vocab_size)
TF-IDF Matrix Shape:  (N_docs × vocab_size)

OHE Sparsity       :  ~XX.X%
BoW Sparsity       :  ~XX.X%
TF-IDF Sparsity    :  ~XX.X%
```

<br/>

---

## 🚀 Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/text-feature-engineering.git
cd text-feature-engineering
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>📋 requirements.txt (click to expand)</summary>

```
numpy
pandas
scikit-learn
nltk
selenium
beautifulsoup4
requests
matplotlib
seaborn
jupyter
```

</details>

### 3. Scrape the Dataset

```bash
# Option A: Run scraper directly
python scraper.py

# Option B: Use the pre-scraped dataset (already in /data)
# Skip this step entirely
```

### 4. Run the Notebook

```bash
jupyter notebook notebook/text_feature_engineering.ipynb
```

> ✅ Run all cells top-to-bottom. Each task is clearly labelled with markdown headers.

<br/>

---

## 📚 Core NLP Concepts

<details>
<summary><b>🔵 One-Hot Encoding (OHE)</b></summary>

<br/>

Represents each document as a binary vector of size `|vocabulary|`. Each position is `1` if the word exists in the document, `0` otherwise.

- **Pros**: Simple, interpretable
- **Cons**: Ignores frequency, highly sparse, no semantic meaning
- **Best for**: Small vocabularies, categorical word presence detection

</details>

<details>
<summary><b>🟡 Bag of Words (BoW)</b></summary>

<br/>

Counts raw word frequencies per document. Two documents with similar meaning but different words look completely different.

- **Pros**: Captures frequency signal, easy to implement
- **Cons**: Ignores word order and semantics, biased toward common words
- **Best for**: Baseline text classification, spam detection

</details>

<details>
<summary><b>🟢 TF-IDF (Term Frequency–Inverse Document Frequency)</b></summary>

<br/>

Weights each word by how often it appears in a document *relative to how rare it is across all documents*. Common words like "the", "is" get lower scores.

```
TF-IDF(t, d) = TF(t, d) × log(N / df(t))
```

- **Pros**: Highlights discriminative, meaningful terms
- **Cons**: Still ignores semantics, order, and context
- **Best for**: Search engines, document ranking, feature extraction

</details>

<details>
<summary><b>⚠️ Why BoW Fails at Semantics</b></summary>

<br/>

Consider these two sentences:
- *"The phone is amazing"*
- *"The smartphone is fantastic"*

BoW sees **zero overlap** in vocabulary — yet they express the same sentiment. Word embeddings (Word2Vec, BERT) solve this, but are beyond the scope of this project.

</details>

<br/>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Tools |
|-------|-------|
| **Scraping** | BeautifulSoup4, Selenium, Requests |
| **Data Handling** | Pandas, NumPy |
| **NLP Preprocessing** | NLTK (tokenizer, stopwords, lemmatizer) |
| **Feature Engineering** | Scikit-learn (CountVectorizer, TfidfVectorizer) |
| **Classification** | Scikit-learn (LogisticRegression, MultinomialNB) |
| **Visualization** | Matplotlib, Seaborn |
| **Notebook** | Jupyter |

</div>

<br/>

---

## 📁 Dataset

- **Source**: Flipkart / Amazon product reviews
- **Size**: 100+ reviews
- **Format**: CSV with columns — `review_text`, `rating`, `sentiment`
- **Language**: English
- **Collection method**: BeautifulSoup / Selenium scraping

> ⚠️ *Data collected in compliance with platform terms of service. No sensitive or restricted content included.*

<br/>

---

## 🔍 Key Learnings

```
✔  Real-world text is noisy — preprocessing is non-negotiable
✔  TF-IDF consistently outperforms raw BoW in classification tasks
✔  Sparse matrices become a serious bottleneck at scale (millions of docs)
✔  OHE is rarely the right choice for large text corpora
✔  No encoding method alone captures true semantic meaning
✔  Logistic Regression + TF-IDF is often a strong, fast baseline
```

<br/>

---

## 📄 Report

A short (1–2 page) report is included at `report.pdf` covering:

- 🔬 Observations from each task
- 📉 Sparsity analysis and memory concerns
- ⚖️ When to use BoW vs TF-IDF in industry
- 🚧 Limitations of TF-IDF in production systems
- 🧭 Recommendations for next steps (embeddings, transformers)


*If you found this useful, drop a ⭐ on the repo!*

<br/>

![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python)
![NLP](https://img.shields.io/badge/Domain-NLP%20%7C%20ML-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>