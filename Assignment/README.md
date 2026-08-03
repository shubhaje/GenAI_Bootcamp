# 📘 Text Feature Engineering using Real-World Product Reviews

## 📖 Project Overview

This project demonstrates a complete **Natural Language Processing (NLP) Text Feature Engineering Pipeline** using real-world product reviews. The objective is to transform unstructured text into meaningful numerical representations that can be used by Machine Learning algorithms for sentiment analysis and text classification.

The project covers the complete workflow—from dataset collection and preprocessing to feature engineering, model training, and performance evaluation.

This project was developed as part of my AI & Machine Learning learning journey to strengthen my understanding of classical NLP techniques before moving to advanced embedding models and Large Language Models (LLMs).

---

# 🎯 Problem Statement

Machine Learning algorithms cannot understand raw text directly. Before training any model, textual data must be converted into numerical features while preserving as much meaningful information as possible.

This project addresses that challenge by implementing and comparing multiple text feature engineering techniques using real-world customer reviews.

---

# 🚀 Project Objectives

* Collect and prepare real-world customer review data
* Perform comprehensive text preprocessing
* Build vocabulary from cleaned text
* Implement and compare:

  * One-Hot Encoding
  * Bag of Words (BoW)
  * TF-IDF
* Analyze sparse matrix representation
* Train baseline Machine Learning models
* Evaluate model performance using standard classification metrics

---

# 📂 Project Structure

```text
Text-Feature-Engineering/
│
├── data/
│   └── reviews_scraped.csv
│
├── screenshots/
│
├── scraper.py
├── generate_dataset.py
├── text_feature_engineering.ipynb
├── README.md
└── requirements.txt
```

---

# 📁 File Description

## 📓 text_feature_engineering.ipynb

Main notebook containing the complete NLP pipeline.

### Includes

* Dataset loading
* Data exploration
* Text preprocessing
* Vocabulary creation
* Feature engineering
* Sparse matrix analysis
* Machine Learning
* Model evaluation
* Performance comparison
* Visualization

---

## 🕷️ scraper.py

Collects real-world product reviews from e-commerce websites.

### Features

* Extracts review text
* Extracts ratings
* Generates sentiment labels
* Saves dataset into CSV format

---

## ⚙️ generate_dataset.py

Generates a synthetic review dataset for offline execution and testing.

### Why this file?

Real-world scraping depends on:

* Internet availability
* Website structure
* Website access permissions

To make the project reproducible and executable on any machine, this script generates realistic customer reviews with ratings and sentiments.

---

## 📂 data/

Contains the review dataset used by the notebook.

Example:

| Product    | Rating | Review                 | Sentiment |
| ---------- | ------ | ---------------------- | --------- |
| Smartphone | 5      | Excellent battery life | Positive  |
| Headphones | 2      | Poor sound quality     | Negative  |

---

## 📊 screenshots/

Contains generated charts and visualizations.

Examples include:

* Most frequent words
* Vocabulary analysis
* Sparse matrix comparison
* Model performance graphs

---

# 🧠 NLP Pipeline

```text
Customer Reviews
        │
        ▼
Load Dataset
        │
        ▼
Text Cleaning
        │
        ▼
Tokenization
        │
        ▼
Stopword Removal
        │
        ▼
Lemmatization
        │
        ▼
Vocabulary Creation
        │
        ▼
Feature Engineering
        │
 ┌──────┼──────────┐
 │      │          │
 ▼      ▼          ▼
One-Hot  BoW     TF-IDF
 │      │          │
 └──────┼──────────┘
        │
        ▼
Machine Learning
        │
        ▼
Evaluation
```

---

# 🧹 Text Preprocessing

The following preprocessing steps are implemented:

* Convert text to lowercase
* Remove punctuation
* Remove digits
* Tokenization
* Stopword removal
* Lemmatization

Example:

**Original Review**

```text
This PHONE is AMAZING!! Battery lasts 24 hours.
```

**Processed Review**

```text
phone amazing battery last hour
```

---

# 📚 Feature Engineering Techniques

## 1️⃣ One-Hot Encoding

Represents whether a word exists in a document.

Example

| good | battery | camera |
| ---- | ------- | ------ |
| 1    | 1       | 0      |

---

## 2️⃣ Bag of Words (BoW)

Represents word frequency.

Example

| good | battery | camera |
| ---- | ------- | ------ |
| 3    | 1       | 0      |

---

## 3️⃣ TF-IDF

Represents word importance based on frequency within a document and rarity across all documents.

Advantages

* Reduces importance of common words
* Highlights meaningful words
* Often improves text classification performance

---

# 📈 Machine Learning Models

The following baseline models are implemented:

* Logistic Regression
* Multinomial Naive Bayes

---

# 📊 Evaluation Metrics

The project evaluates models using:

* Accuracy
* Precision
* Recall
* F1-Score
* Classification Report

---

# 📦 Technologies Used

### Programming Language

* Python 3.x

### Libraries

* Pandas
* NumPy
* NLTK
* Scikit-learn
* Matplotlib

---

# 💡 Key Learning Outcomes

This project helped me understand:

* Complete NLP preprocessing workflow
* Vocabulary creation
* Feature Engineering techniques
* Differences between One-Hot Encoding, Bag of Words, and TF-IDF
* Sparse matrix representation
* Traditional Machine Learning for text classification
* Importance of preprocessing before applying ML models

---

# 🔮 Future Enhancements

Future improvements may include:

* Word2Vec
* FastText
* GloVe
* Sentence Transformers
* BERT Embeddings
* Transformer-based Sentiment Classification
* Vector Databases (FAISS / ChromaDB)
* Retrieval-Augmented Generation (RAG)
* LLM-powered text classification

---

# ▶️ How to Run

## 1. Clone the repository

```bash
git clone <repository-url>
cd Text-Feature-Engineering
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Generate dataset (Optional)

```bash
python generate_dataset.py
```

or collect real-world reviews

```bash
python scraper.py
```

## 4. Launch Jupyter Notebook

```bash
jupyter notebook text_feature_engineering.ipynb
```

Run all cells sequentially.

---

# 📌 Skills Demonstrated

* Python Programming
* Natural Language Processing (NLP)
* Data Preprocessing
* Text Feature Engineering
* Machine Learning
* Data Visualization
* Model Evaluation
* Software Engineering Best Practices

---

# 👩‍💻 About the Project

This project was developed to build a strong foundation in classical NLP and text feature engineering. While modern AI models such as BERT and Large Language Models generate contextual embeddings automatically, understanding traditional techniques like One-Hot Encoding, Bag of Words, and TF-IDF is essential for appreciating how text representation has evolved and for solving many practical NLP problems.

---

# ⭐ If you found this project useful

If this repository helps you learn NLP or Text Feature Engineering, consider giving it a ⭐ on GitHub.
