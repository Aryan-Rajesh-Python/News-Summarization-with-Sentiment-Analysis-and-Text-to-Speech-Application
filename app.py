import requests
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
from gtts import gTTS
from transformers import pipeline

# API Key (Replace with your own NewsAPI Key)
NEWS_API_KEY = "5c5ea7ba872146b9b4eab7f9b6b28b10"

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to fetch news
def fetch_news(company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}&language=en&pageSize=5"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    articles = data.get("articles", [])
    news_list = []
    
    for article in articles:
        title = article.get("title", "No Title")
        content = article.get("content", article.get("description", "No Content Available"))
        
        try:
            summary = summarizer(content, max_length=100, min_length=50, do_sample=False)[0]['summary_text']
        except:
            summary = "Summary not available."
        
        sentiment = analyze_sentiment(title)
        topics = extract_topics(title + " " + summary)
        
        news_list.append({
            "Title": title,
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topics
        })
    
    return news_list

# Sentiment Analysis
def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Extract Topics (Simple Keyword Extraction)
def extract_topics(text):
    keywords = text.split()[:5]  # Taking first 5 keywords as topics (Can be improved with NLP models)
    return list(set(keywords))

# Compare Articles
def compare_articles(articles):
    comparisons = []
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    topic_overlap = {"Common Topics": [], "Unique Topics in Article 1": [], "Unique Topics in Article 2": []}
    
    if len(articles) < 2:
        return {}, []
    
    for article in articles:
        sentiments[article["Sentiment"]] += 1
    
    topic_overlap["Common Topics"] = list(set(articles[0]["Topics"]) & set(articles[1]["Topics"]))
    topic_overlap["Unique Topics in Article 1"] = list(set(articles[0]["Topics"]) - set(articles[1]["Topics"]))
    topic_overlap["Unique Topics in Article 2"] = list(set(articles[1]["Topics"]) - set(articles[0]["Topics"]))
    
    comparisons.append({
        "Comparison": f"Article 1 talks about {', '.join(articles[0]['Topics'])}, while Article 2 focuses on {', '.join(articles[1]['Topics'])}.",
        "Impact": "One article is more market-focused, while the other highlights risks."
    })
    
    return sentiments, comparisons, topic_overlap

# Text to Speech (Hindi)
def text_to_speech(text):
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)
    hindi_tts = gTTS(text=translated_text, lang="hi")
    hindi_file = "news_summary_hindi.mp3"
    hindi_tts.save(hindi_file)
    return hindi_file

# Streamlit UI
st.title("📰 News Sentiment & Analysis")
company = st.text_input("Enter Company Name")

if st.button("Fetch News"):
    articles = fetch_news(company)
    
    if not articles:
        st.error("No news articles found.")
    else:
        sentiments, comparisons, topic_overlap = compare_articles(articles)
        final_sentiment = "Mostly Positive" if sentiments["Positive"] > sentiments["Negative"] else "Mixed" if sentiments["Positive"] == sentiments["Negative"] else "Mostly Negative"
        full_text = " ".join([f"{art['Title']}: {art['Summary']}" for art in articles])
        hindi_audio = text_to_speech(full_text)
        
        output = {
            "Company": company,
            "Articles": articles,
            "Comparative Sentiment Score": {
                "Sentiment Distribution": sentiments,
                "Coverage Differences": comparisons,
                "Topic Overlap": topic_overlap
            },
            "Final Sentiment Analysis": f"{company}’s latest news coverage is {final_sentiment}.",
            "Audio": "[Play Hindi Speech]"
        }
        
        st.json(output)
        st.audio(hindi_audio)
