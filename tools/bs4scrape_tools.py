import json
import requests
import streamlit as st
from langchain.tools import tool
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus.common import thai_stopwords
import string

class ScrapeTools:

  @tool("Scrape and Summarize Website")
  def scrape_and_summarize_website(url):
    """Scrapes and summarizes website content using BeautifulSoup."""
    try:
        # Fetch HTML content
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch {url}. Status code: {response.status_code}"

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs])
        return content[:8000]  # Return the first 8000 characters

    except Exception as e:
        return f"Error scraping website: {str(e)}"

  @tool("Extract Metadata and Keywords")
  def extract_metadata_and_keywords(url):
    """Extracts metadata and keywords from the given URL."""
    try:
        # Fetch HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        title = soup.title.string if soup.title else "No Title"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc.get("content", "") if meta_desc else "No Description"

        # Extract and preprocess keywords
        texts = soup.get_text().lower()
        tokens = word_tokenize(texts, keep_whitespace=False)  # Tokenization
        stopwords = set(thai_stopwords())  # Load Thai stopwords
        tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
        keywords = pd.Series(tokens).value_counts().head(20)

        return {
            "title": title,
            "description": description,
            "keywords": keywords.to_dict()
        }
    except Exception as e:
        return f"Error extracting metadata and keywords: {str(e)}"

  @tool("Compare Keyword Similarity")
  def compute_keyword_similarity(keywords1, keywords2):
    """Computes cosine similarity between two sets of keywords using TF-IDF."""
    try:
        # Use TF-IDF instead of CountVectorizer
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([keywords1, keywords2])
        similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        return similarity
    except Exception as e:
        return f"Error computing similarity: {str(e)}"
