import os
import time
import requests
from celery.schedules import crontab
from celery import Celery
from pymongo import MongoClient


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/news_db")

client = MongoClient(MONGO_URI)
db = client["news_db"]
news_collection = db["news"]

news_collection.create_index("url", unique=True)

NEWS_API_KEY = "47df54ee6db24028b2fcd4c4cc640bf3"
NEWS_API_URL = f"https://newsapi.org/v2/everything?q=superbowl&apiKey={NEWS_API_KEY}"


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y

@celery.task(name="tasks.fetch_news")
def fetch_news():
    """Fetches Superbowl news and stores it in MongoDB without duplicates."""
    try:
        response = requests.get(NEWS_API_URL)
        data = response.json()

        if data["status"] == "ok":
            articles = data.get("articles", [])
            inserted_count = 0

            for article in articles:
                news_data = {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"], 
                    "image_url":article["urlToImage"],
                    "source": article["source"]["name"],
                    "published_at": article["publishedAt"],
                }

                existing_article = news_collection.find_one({"url": news_data["url"]})
                print(existing_article)
                if not existing_article:
                    news_collection.insert_one(news_data)
                    inserted_count += 1

            return f"Fetched {len(articles)} articles, inserted {inserted_count} new articles."
        else:
            return f"Error from NewsAPI: {data}"
    
    except Exception as e:
        return f"Error fetching news: {str(e)}"
    
celery.conf.beat_schedule = {
    "fetch-news-every-30-minutes": {
        "task": "tasks.fetch_news",
        "schedule": crontab(minute="*/15"), 
    },
}