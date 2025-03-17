# News Summarization with Sentiment Analysis and Text-to-Speech Application

This project provides a tool for fetching the latest news, summarizing it, performing sentiment analysis, and converting the summary into audio in both English and Hindi using **Python**, **Streamlit**, **TextBlob**, **Google Text-to-Speech (gTTS)**, **Deep Translator**, and **Transformers**.

## Features

- **News Fetching**: Fetch the latest news articles about a specific company using NewsAPI.
- **Summarization**: Automatically summarize the fetched articles for quick reading.
- **Sentiment Analysis**: Analyze the sentiment (Positive, Negative, or Neutral) of the news titles.
- **Text-to-Speech (TTS)**: Convert the summarized text into speech in both **English** and **Hindi** using gTTS.
- **Parallel Processing**: Improve performance by handling TTS and translation in parallel.

## Requirements

Before running the project, make sure you have the following Python packages installed. You can use the `requirements.txt` file to install them using pip.

```txt
streamlit
requests
textblob
gtts
deep-translator
transformers
torch
sentencepiece
