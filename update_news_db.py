from database_manager import DatabaseManager as DB
from news_scraper import NewsScraper

NewsScraper.update_news_db()
#NewsScraper.scrape("MANILABULLETIN","http://mb.com.ph/mb-feed/", "six_months_before", "earliest_date");
#NewsScraper.scrape("GMA",'http://www.gmanetwork.com/news/rss/news/money', "six_months_before", "earliest_date");