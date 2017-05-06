from create_db import db, News, Word, Topic
from database_manager import DatabaseManager as DB

sentiment_dictionary = {}

class SentimentAnalyzer:
    def __init__(self):
        for line in open('../resources/word_sentiments_2.txt'):
            word, score = line.split(' ')
            sentiment_dictionary[word] = int(score)

    def identify_reliability(self, news):
        mean_topic, variance_topic = self.compute_sentiment_variance_per_topic(news.topic)
        if news.topic == None or variance_topic < 0.01:
            return 0

        news_sentiment = self.compute_sentiment_news(news)
        topic_sentiment = self.compute_sentiment_per_topic(news.topic)
        score_reliability =  100 - abs(topic_sentiment - news_sentiment) * 10000

        print("")
        print("average topic sentiment: " + str(topic_sentiment))
        print("input news sentiment: " + str(news_sentiment))
        print("")
        
        if news_sentiment > topic_sentiment:
            return 1
        else:
            return 0
    
    def compute_sentiment_news(self, news):
        sum = 0
        count = 0
        
        if not news.sentiment is None:
            return news.sentiment

        for news_word in news.news_words:
            word_sentiment = sentiment_dictionary.get(news_word.word.word.lower(),0)
            word_sentiment = news_word.word_count * word_sentiment
            sum = sum + word_sentiment
            count += news_word.word_count
            
        mean = 0
        if count != 0:
            mean = sum / count
            
        news.sentiment = sum
        DB.commit_db()
        return sum


    def compute_sentiment_per_topic(self, topic):
        sum = 0
        count = 0
        topic_newslist = topic.newslist.all()

        for news in topic_newslist:
            sentiment = self.compute_sentiment_news(news)
            #print("news in topic count" + str(count) + " " + str(sentiment))
            sum = sum + self.compute_sentiment_news(news)
            count += 1
        mean = 0
        if count != 0:
            mean = sum / count
        return mean

    def compute_variance_per_topic(self, topic):
        score = 0
        scores = []
        news_count = len(topic.newslist.all())
        
        sum = 0
        count = 0
        topic_newslist = topic.newslist.all()

        for news in topic.newslist:
            score = score + self.compute_sentiment_news(news)
            scores.append(score)
            
            sum = sum + self.compute_sentiment_news(news)
            count += 1

        mean = score / len(topic.newslist.all())

        for score in scores:
            variance = int((score - mean))^2

        variance = variance/news_count
        return variance
    
    def compute_sentiment_variance_per_topic(self, topic):
        score = 0

        scores = []
        news_count = len(topic.newslist.all())

        for news in topic.newslist:
            score = score + self.compute_sentiment_news(news)
            scores.append(score)

        mean = score / news_count

        for score in scores:
            variance = int((score - mean))^2

        variance = variance/news_count
        return (mean, variance)