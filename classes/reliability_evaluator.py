import sys 
sys.path.append('..')

from create_db import db,News, Topic, InputNews, NewsWord, Word
from sentiment_analyzer import SentimentAnalyzer
from news_scraper import NewsScraper
from datetime import date
from dateutil.relativedelta import relativedelta
from natural_language_processor import NaturalLanguageProcessor as NLP
from database_manager import DatabaseManager as DB
from topic_generator import TopicGenerator

number_of_top_words = 20
minimum_match_word = 2

class ReliabilityEvaluator:
    sentiment_analyzer = None
    topic_generator = None
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.topic_generator = TopicGenerator(self)
        print("Reliability Evaluator Initialization")
    
    #RELIABILITY COMPUTATION METHODS
    def compute_for_reliability_score(self, input_string):
        input_news = News("pubdate", "link", input_string, NLP.count_occurrence(input_string))

        if not self.identify_topic_for_news(input_news) == None:
            reliability = self.sentiment_analyzer.identify_reliability(input_news)
            return reliability
        else:
            print("No topic")
            return None

    def compute_for_reliability_score_input_news(self, input_string):
        input_news = InputNews("pubdate", "link", input_string, NLP.input_count_occurrence(input_string))

        if not self.topic_generator.identify_topic_for_news(input_news) == None:
            reliability = self.sentiment_analyzer.identify_reliability(input_news)
            return reliability
        else:
            print("No topic")
            return None
        
    def compute_reliability_input_news(self):
        input_news_list = InputNews.query.all()
        for input_news in input_news_list:
            self.compute_for_reliability_score_input_news(input_news.content)
            
    def compute_reliability_article_news(self):
        input_news_list = InputNews.query.all()
        for input_news in input_news_list:
            self.compute_for_reliability_score_input_news(input_news.content)

    #SCRAPING METHODS
    def scrape_news_starting_from(self,date):
        channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
        rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
            'RAPPLER': 'http://feeds.feedburner.com/rappler/',
            'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
            'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
            'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

        #scrape news from 6 months ago
        for i in range(0,5): 
            NewsScraper.scrape(channels[i], rssurl[channels[i]], date, "20170301");
    
    #TOPIC GENERATION METHODS      
    def generate_topics(self):
        self.generate_article_news_topics()
        self.generator_input_news_topics()
        
    def generate_article_news_topics(self):
        self.topic_generator.generate_topics()
        
    def generator_input_news_topics(self):
        self.topic_generator.get_topics_of_input_news_content()

        
rel = ReliabilityEvaluator()
rel.compute_reliability_article_news()

