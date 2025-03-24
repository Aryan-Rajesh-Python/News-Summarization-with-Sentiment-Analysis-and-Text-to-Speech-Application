# 🚀 News Summarization & Sentiment Analysis with Text-to-Speech

This intelligent news processing application fetches real-time news, extracts key insights, analyzes sentiment, identifies core topics, and delivers audio summaries in **Hindi**. Designed for efficiency, it leverages **AI-driven summarization, sentiment detection, and multilingual speech synthesis** to provide a seamless news consumption experience.

## ✨ Features

🔹 **Real-Time News Fetching** – Get the latest updates on any company or topic using NewsAPI.  
🔹 **AI-Powered Summarization** – Distills lengthy articles into concise, easy-to-digest summaries.  
🔹 **Sentiment Analysis** – Classifies news articles as **Positive, Negative, or Neutral** to assess market sentiment.  
🔹 **Topic Extraction** – Identifies key themes covered in news reports.  
🔹 **Comparative Analysis** – Highlights key differences and overlaps between articles.  
🔹 **Hindi Text-to-Speech (TTS)** – Converts news summaries into **Hindi audio** for effortless listening.  
🔹 **Optimized Performance** – Utilizes parallel processing for faster execution and improved efficiency.

## 🔧 Installation & Setup

Ensure you have Python installed, then install dependencies using:

```sh
pip install -r requirements.txt
```

## 📦 Requirements

- `streamlit` – Interactive UI for seamless experience  
- `requests` – Fetch real-time news from APIs  
- `textblob` – Sentiment analysis of headlines  
- `gtts` – Convert text summaries into Hindi speech  
- `deep-translator` – Translate summaries for multilingual TTS  
- `transformers` – AI-based summarization and text processing  
- `torch` – Backend for transformer models    
- `scikit-learn` – Data processing and analysis utilities  

## 🚀 Usage

Run the Streamlit app with:

```sh
streamlit run app.py
```

1️⃣ **Enter a company name or topic** to fetch related news.  
2️⃣ **View summarized news** along with sentiment classification.  
3️⃣ **Listen to news summaries** in **Hindi** with TTS.  
4️⃣ **Analyze comparative insights** between different articles.  

## 🌍 Future Enhancements

✅ Support for additional languages in text-to-speech  
✅ Integration with more news sources for broader coverage  
✅ Advanced NLP techniques for improved summarization accuracy  
✅ Interactive sentiment trend visualization over time  
