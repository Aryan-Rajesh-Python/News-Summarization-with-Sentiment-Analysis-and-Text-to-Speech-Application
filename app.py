import requests
import streamlit as st
from textblob import TextBlob
import os
from gtts import gTTS
from deep_translator import GoogleTranslator

# NewsAPI Key
NEWS_API_KEY = "5c5ea7ba872146b9b4eab7f9b6b28b10"

# Function to fetch news from NewsAPI
def fetch_news(company):
    """ Fetch news articles related to the company using NewsAPI. """
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={NEWS_API_KEY}&language=en&pageSize=5"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("articles", [])

    news_list = []
    for article in articles:
        news_list.append({
            "title": article["title"],
            "description": article.get("description", ""),
            "url": article["url"]
        })

    return news_list

# Function for sentiment analysis
def analyze_sentiment(text):
    """ Classifies sentiment as Positive, Negative, or Neutral. """
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to Convert Text to Both English & Hindi Speech
def text_to_speech(text):
    """ Converts text into both English and Hindi speech using gTTS (Cloud-based TTS). """
    
    # ✅ English Voice (Using gTTS)
    english_tts = gTTS(text=text, lang="en")
    english_file = "output_english.mp3"
    english_tts.save(english_file)

    # ✅ Translate English to Hindi
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)

    # ✅ Hindi Voice (Using gTTS)
    hindi_tts = gTTS(text=translated_text, lang="hi")
    hindi_file = "output_hindi.mp3"
    hindi_tts.save(hindi_file)

    return english_file, hindi_file
    
# Streamlit UI
st.title("📰 News Summarization and Text-to-Speech")
company = st.text_input("Enter Company Name")

if st.button("Fetch News"):
    articles = fetch_news(company)

    if not articles:
        st.error("No news articles found. Try a different company.")
    else:
        full_text = ""
        for news in articles:
            title = news["title"]
            sentiment = analyze_sentiment(title)

            st.subheader(title)
            st.write(f"**Sentiment:** {sentiment}")
            st.write(f"[Read More]({news['url']})")

            full_text += f"{title} - Sentiment: {sentiment}. "

        # Convert summary to both English & Hindi speech
        english_speech, hindi_speech = text_to_speech(full_text)

        # Play English Audio (Default)
        st.subheader("🔊 English News")
        st.audio(english_speech)

        # Play Hindi Audio (Translated)
        st.subheader("🔊 Hindi News")
        st.audio(hindi_speech)
