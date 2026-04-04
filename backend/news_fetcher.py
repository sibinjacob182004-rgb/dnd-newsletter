import os
import requests
import feedparser
from datetime import datetime

from backend.utils.logger import logger

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# Keywords for filtering
POSITIVE_KEYWORDS = ["ai", "machine learning", "data science", "deep learning", "nlp"]
NEGATIVE_KEYWORDS = ["politics", "sports", "crime", "celebrity"]


# -----------------------------
# 🔹 GNEWS FETCH
# -----------------------------
def fetch_from_gnews():
    url = "https://gnews.io/api/v4/search"

    params = {
        "q": "data science OR AI OR machine learning OR big data",
        "lang": "en",
        "max": 10,
        "apikey": GNEWS_API_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    articles = []

    for item in data.get("articles", []):
        articles.append({
            "title": item.get("title"),
            "summary": item.get("description"),
            "url": item.get("url"),
            "source": item.get("source", {}).get("name"),
            "published_date": item.get("publishedAt")
        })

    return articles


# -----------------------------
# 🔹 RSS FETCH
# -----------------------------
RSS_FEEDS = [
    "https://towardsdatascience.com/feed",
    "https://www.kdnuggets.com/feed",
    "https://www.analyticsvidhya.com/blog/feed/"
]


def fetch_from_rss():
    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.get("title"),
                "summary": entry.get("summary", "")[:200],
                "url": entry.get("link"),
                "source": feed.feed.get("title"),
                "published_date": entry.get("published", str(datetime.now()))
            })

    return articles


# -----------------------------
# 🔹 FILTERING LOGIC
# -----------------------------
def is_relevant(article):
    text = (article["title"] + " " + (article["summary"] or "")).lower()

    if any(neg in text for neg in NEGATIVE_KEYWORDS):
        return False

    score = sum(1 for pos in POSITIVE_KEYWORDS if pos in text)

    return score >= 1


def filter_articles(articles):
    filtered = [a for a in articles if is_relevant(a)]
    return filtered


# -----------------------------
# 🔹 MAIN PIPELINE FUNCTION
# -----------------------------
def fetch_all_news():
    all_articles = []

    # GNews
    try:
        logger.info("📡 Fetching from GNews...")
        gnews_articles = fetch_from_gnews()
        logger.info(f"📰 GNews articles: {len(gnews_articles)}")
    except Exception as e:
        logger.error(f"❌ GNews error: {e}")
        gnews_articles = []

    # RSS
    try:
        logger.info("📡 Fetching from RSS...")
        rss_articles = fetch_from_rss()
        logger.info(f"📰 RSS articles: {len(rss_articles)}")
    except Exception as e:
        logger.error(f"❌ RSS error: {e}")
        rss_articles = []

    # Combine
    all_articles.extend(gnews_articles)
    all_articles.extend(rss_articles)

    logger.info(f"📊 Total before filtering: {len(all_articles)}")

    # Filter
    filtered = filter_articles(all_articles)

    logger.info(f"✅ After filtering: {len(filtered)}")

    return filtered