import requests
import bs4
import logging
import os
import gtts
from textblob import TextBlob

# Setup logging
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def fetch_news(company_name):
    """Fetch news articles related to a company using BeautifulSoup"""
    search_url = f"https://news.google.com/search?q={company_name}"
    response = requests.get(search_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    
    articles = []
    for item in soup.find_all("article")[:10]:  # Extract 10 articles
        title = item.find("h3")
        if title:
            summary = item.find("p").text if item.find("p") else "No summary available"
            articles.append({"title": title.text, "summary": summary})
    
    return articles

def analyze_sentiment(text):
    """Perform sentiment analysis"""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    return "Neutral"

def generate_tts(text, output_file="output.mp3"):
    """Convert text to Hindi speech"""
    tts = gtts.gTTS(text, lang="hi")
    tts.save(output_file)
    return output_file
