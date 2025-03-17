import requests
import streamlit as st
from textblob import TextBlob
import os
from gtts import gTTS
from deep_translator import GoogleTranslator
from transformers import pipeline
import concurrent.futures

# NewsAPI Key
NEWS_API_KEY = "5c5ea7ba872146b9b4eab7f9b6b28b10"

# Use a Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Cache API Responses to Reduce Load
@st.cache_data
def fetch_news(company):
    """ Fetch news articles, summarize them, and return structured data. """
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}&language=en&pageSize=5"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("articles", [])

    news_list = []
    for article in articles:
        full_text = article.get("content", article.get("description", "No full article available."))

        try:
            # Reduce Summary Length for Faster Processing
            summary = summarizer(full_text, max_length=150, min_length=80, do_sample=False)[0]['summary_text']
        except:
            summary = "Summary not available."

        news_list.append({
            "title": article["title"],
            "summary": summary,  # Store summarized text
            "url": article["url"]
        })

    return news_list

# Function for Sentiment Analysis
def analyze_sentiment(text):
    """ Classifies sentiment as Positive, Negative, or Neutral. """
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Optimized Parallel Processing for TTS & Translation
def text_to_speech(text):
    """ Converts text into both English and Hindi speech in parallel using threads. """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        # English TTS (Runs in Parallel)
        english_future = executor.submit(gTTS, text=text, lang="en")
        english_tts = english_future.result()
        english_file = "output_english.mp3"
        english_tts.save(english_file)

        # Batch Translate to Hindi (Faster)
        hindi_translation_future = executor.submit(GoogleTranslator(source="en", target="hi").translate, text)
        translated_text = hindi_translation_future.result()

        # Hindi TTS (Runs in Parallel)
        hindi_future = executor.submit(gTTS, text=translated_text, lang="hi")
        hindi_tts = hindi_future.result()
        hindi_file = "output_hindi.mp3"
        hindi_tts.save(hindi_file)

    return english_file, hindi_file

# Streamlit UI
st.title("📰 News Summarization & Sentiment Analysis with TTS")
company = st.text_input("Enter Company Name")

if st.button("Fetch News"):
    articles = fetch_news(company)

    if not articles:
        st.error("No news articles found. Try a different company.")
    else:
        full_text = ""
        for news in articles:
            title = news["title"]
            summary = news["summary"]
            sentiment = analyze_sentiment(title)

            st.subheader(title)
            st.write(f"**Summary:** {summary}")
            st.write(f"**Sentiment:** {sentiment}")
            st.write(f"[Read Full Article]({news['url']})")

            full_text += f"{title}: {summary}. "

        # Convert summarized text to English & Hindi speech (Parallel Processing)
        english_speech, hindi_speech = text_to_speech(full_text)

        # Play English Audio (Default)
        st.subheader("🔊 English News")
        st.audio(english_speech)

        # Play Hindi Audio (Translated)
        st.subheader("🔊 Hindi News")
        st.audio(hindi_speech)
