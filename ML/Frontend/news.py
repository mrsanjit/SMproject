import requests
from bs4 import BeautifulSoup
import streamlit as st

def fetch_health_articles():
    # URL to scrape health news from Healthline
    url = "https://www.healthline.com/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the headlines (you might need to update this depending on the website structure)
        headlines = soup.find_all("h2", class_="article-card-title")

        # If we find articles, display them
        if headlines:
            st.header("Latest Health News and Articles")
            for headline in headlines[:10]:  # Limiting to the first 10 headlines
                st.subheader(headline.get_text(strip=True))
        else:
            st.warning("No headlines found.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching news: {e}")
