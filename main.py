# -*- coding: utf-8 -*-
"""nlp_assignment-2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/fatmaahhmed/5ce769653615ed434990bc626ef8a76e/nlp_assignment-2.ipynb

**Fatma Ahmed Abdulfadeel    20200373**

**Hamed Osama                20200138**

**Ziad Essam                 20200202**
"""

import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

"""# **Documents Generation**"""

from transformers import pipeline

# Initialize the text generation pipeline with the desired model
generator = pipeline('text-generation', model='gpt2')

# Generate first document
doc1 = generator('Artifitial Intelligence', max_length=1000, num_return_sequences=1,truncation=True)
doc1 = doc1[0]['generated_text']

doc1

# Generate second document
doc2 = generator('Generative AI', max_length=1000, num_return_sequences=1,truncation=True)
doc2 = doc2[0]['generated_text']

doc2

# Generate third document
doc3 = generator('Machine Learning', max_length=1000, num_return_sequences=1,truncation=True)
doc3 = doc3[0]['generated_text']

doc3

"""# **Documents Preprocessing**"""

def process_text(text):
    # Cleaning data from each symbol or character doesn’t contain to the data
    text = re.sub(r'[^\w\s]', '', text)

    # Normalization: make all the data to lower case
    text = text.lower()

    # Tokenization: split the data to words
    words = word_tokenize(text)

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Stop words removal
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    return words

doc1_process = process_text(doc1)
doc1_process

doc2_process = process_text(doc2)
doc2_process

doc3_process = process_text(doc3)
doc3_process

corpus = [doc1_process, doc2_process, doc3_process]
corpus

"""# **TF_IDF From Scratch**"""

def calculate_tf(document):
    tf_document = {}
    word_count = len(documnt)
    word_freq = Counter(document)
    for word, freq in word_freq.items():
        tf_document[word] = freq / word_count
    return tf_document

TF = [calculate_tf(document) for document in corpus]
TF

# Calculate Inverse Document Frequency (IDF)
def calculate_idf(documents):
    N = len(documents)
    idf = {}
    for document in documents:
        for word in document:
            if word not in idf:
                count = sum(1 for doc in documents if word in doc)
                idf[word] = math.log(N / count + 1) + 1

    return idf

IDF = [calculate_idf(document) for document in corpus]
IDF

# Calculate TF-IDF
def calculate_tfidf(tf, idf):
    tfidf_documents = []
    for tf_document, idf_values in zip(tf, idf):
        tfidf_document = {}
        for word, tf_val in tf_document.items():
            tfidf_document[word] = tf_val * idf_values[word] if word in idf_values else 0
        tfidf_documents.append(tfidf_document)
    return tfidf_documents

import math

def normalize_tfidf(tfidf):
    squared_sum = sum(tf_val ** 2 for tf_val in tfidf.values())
    norm = math.sqrt(squared_sum)
    if norm == 0:
        return {word: 0 for word in tfidf}
    normalized_tfidf = {word: tf_val / norm for word, tf_val in tfidf.items()}
    return normalized_tfidf

TFIDF_Normalized = [normalize_tfidf(document) for document in TF_IDF]

TFIDF_Normalized

"""# **TF_IDF Built in (Bonus)**"""

# Joining preprocessed documents into single strings
corpus_strings = [' '.join(doc) for doc in corpus]

# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit into TF-IDF features
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus_strings)

# feature names
feature_names = tfidf_vectorizer.get_feature_names_out()

# Print TF-IDF values
for idx, doc in enumerate(tfidf_matrix.toarray(), start=1):
    print(f"TF-IDF for Document {idx}:")
    print("{")
    for word_idx, tfidf in enumerate(doc):
        word = feature_names[word_idx]
        print(f"    '{word}': {tfidf},")
    print("}")
    print()
