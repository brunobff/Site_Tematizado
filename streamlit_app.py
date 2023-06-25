# -*- coding: utf-8 -*-
"""Sistema_Avaliacao_Criticas_Web.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Omc3XVFSRBhF0OgkAI1b31n9qaCKk1HX

# Sistema de classificação de sentimentos de críticas de produtos vendidos pela Amazon
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.request import urlopen
from sklearn.svm import SVC
from textblob import TextBlob
import streamlit as st
from transformers import pipeline   
from PIL import Image

@st.cache_data
def load_data():
    data = pd.read_json(arquivo)
    return data

arquivo = 'https://raw.githubusercontent.com/BFFgit/Sistema_Avaliacao_Criticas/main/data_class_web.json'

data = load_data()

st.sidebar.image("https://raw.githubusercontent.com/BFFgit/Sistema_Avaliacao_Criticas/main/Amazon_logo.svg", use_column_width=True)

st.markdown("<h1 style='text-align: center; color: orange;'>Análise de Sentimento de Críticas de Produtos</h1>", unsafe_allow_html=True)

st.write(data)
st.caption('Dataset de Críticas da Amazon')

nltk.download('punkt')  
nltk.download('stopwords')

model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
classifier = pipeline('sentiment-analysis', model=model_name)

stop_words = set(stopwords.words('english'))

def preprocess_text(texto):
    tokens = word_tokenize(texto.lower())
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Vetorização de texto usando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['preprocessed_text'])
y = data['Sentiment']

# Treinamento do modelo SVM
classifier = SVC(kernel='linear')
classifier.fit(X, y)

# Função para realizar a classificação de sentimentos
def analisar_sentimento(texto):
    preprocessed_text = preprocess_text(texto)
    text_vector = vectorizer.transform([preprocessed_text])
    sentiment = classifier.predict(text_vector)[0]
    return sentiment

# Exemplo de uso
texto = st.text_input("Digite sua crítica:")
if st.button("Analisar Crítica"):
    sentimento = analisar_sentimento(texto)
    st.write(f"Crítica Escrita: {texto}")
    st.write(f"Classificação: {sentimento}")
    if sentimento == " Crítica Positiva":
        imagem = 'https://raw.githubusercontent.com/BFFgit/Sistema_Avaliacao_Criticas/main/Rotten_Tomatoes.svg'
        st.image(imagem)
    else:
        imagem = 'https://raw.githubusercontent.com/BFFgit/Sistema_Avaliacao_Criticas/main/Rotten_Tomatoes_rotten.svg'
        st.image(imagem)
