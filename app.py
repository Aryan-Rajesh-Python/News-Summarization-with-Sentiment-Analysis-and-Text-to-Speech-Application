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
        
        sentiment = analyze_sentiment(title + " " + summary)
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

# Extract Topics (Improved)
def extract_topics(text):
    words = text.split()
    keywords = list(set(words))[:5]  # Unique first 5 keywords
    return keywords

# Compare Articles (Full Pairwise Comparison)
def compare_articles(articles):
    comparisons = []
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    all_topics = []
    
    for article in articles:
        sentiments[article["Sentiment"]] += 1
        all_topics.append(set(article["Topics"]))
    
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            common_topics = list(all_topics[i] & all_topics[j])
            unique_topics_1 = list(all_topics[i] - all_topics[j])
            unique_topics_2 = list(all_topics[j] - all_topics[i])
            
            comparisons.append({
                "Comparison": f"Article {i+1} talks about {', '.join(articles[i]['Topics'])}, while Article {j+1} focuses on {', '.join(articles[j]['Topics'])}.",
                "Impact": "Different focus areas identified in these articles."
            })
    
    return sentiments, comparisons

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
        sentiments, comparisons = compare_articles(articles)
        final_sentiment = "Mostly Positive" if sentiments["Positive"] > sentiments["Negative"] else "Mixed" if sentiments["Positive"] == sentiments["Negative"] else "Mostly Negative"
        full_text = " ".join([f"{art['Title']}: {art['Summary']}" for art in articles])
        hindi_audio = text_to_speech(full_text)
        
        output = {
            "Company": company,
            "Articles": articles,
            "Comparative Sentiment Score": {
                "Sentiment Distribution": sentiments,
                "Coverage Differences": comparisons
            },
            "Final Sentiment Analysis": f"{company}’s latest news coverage is {final_sentiment}.",
            "Audio": "[Play Hindi Speech]"
        }
        
        st.json(output)
        st.audio(hindi_audio)
