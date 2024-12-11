import sys
from collections import defaultdict, Counter
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
from bs4 import BeautifulSoup
import requests

# Add necessary paths
sys.path.append('/path/to/dependencies')

# Regular Expressions for text cleaning
SPECIAL_CHARS = re.compile(r'[^\w\s]')

# Stopwords and common nouns
COMMON_NOUNS = set("january february ...".split())
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    """Clean text and remove unwanted characters."""
    words = word_tokenize(text.lower())
    return [SPECIAL_CHARS.sub("", word) for word in words if word not in STOPWORDS and word not in COMMON_NOUNS]

def scrape_webpage(url):
    """Fetch and parse webpage content."""
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(), soup

def extract_features(text):
    """Extract and score keywords."""
    words = clean_text(text)
    word_freq = Counter(words)
    return word_freq.most_common(10)

if __name__ == "__main__":
    url = input("Enter a URL: ")
    raw_text, _ = scrape_webpage(url)
    keywords = extract_features(raw_text)
    print("Top Keywords:", keywords)
